package main

import (
	"bytes"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
)

func main() {
	app := fiber.New()

	// CORS middleware
	app.Use(cors.New(cors.Config{
		AllowOrigins: "http://localhost:3000",
		AllowHeaders: "Origin, Content-Type, Accept",
		AllowMethods: "GET, POST, PUT, DELETE, OPTIONS",
	}))

	// Route
	app.Post("/api/upload", handleUpload)

	fmt.Println("Fiber backend running on http://localhost:8080")
	if err := app.Listen(":8080"); err != nil {
		panic(err)
	}
}

func handleUpload(c *fiber.Ctx) error {
	// 1. Read job description
	jobDesc := c.FormValue("job_description")

	// 2. Read multipart form
	form, err := c.MultipartForm()
	if err != nil {
		return fiber.NewError(fiber.StatusBadRequest, "Invalid multipart form")
	}
	files := form.File["resumes"]
	if len(files) == 0 {
		return fiber.NewError(fiber.StatusBadRequest, "No resume files found")
	}

	// 3. Build new multipart request for Flask
	var buf bytes.Buffer
	writer := multipart.NewWriter(&buf)

	if err := writer.WriteField("job_description", jobDesc); err != nil {
		return fiber.NewError(fiber.StatusInternalServerError, "Failed to write job description")
	}

	for _, fh := range files {
		f, err := fh.Open()
		if err != nil {
			return fiber.NewError(fiber.StatusInternalServerError, "Failed to open uploaded file")
		}
		part, err := writer.CreateFormFile("resumes", fh.Filename)
		if err != nil {
			f.Close()
			return fiber.NewError(fiber.StatusInternalServerError, "Failed to create form file")
		}
		if _, err := io.Copy(part, f); err != nil {
			f.Close()
			return fiber.NewError(fiber.StatusInternalServerError, "Failed to copy file content")
		}
		f.Close()
	}
	writer.Close() // important!

	// 4. Proxy to Flask
	req, err := http.NewRequest("POST", "http://localhost:5000/matcher", &buf)
	if err != nil {
		return fiber.NewError(fiber.StatusInternalServerError, "Failed to create HTTP request")
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	client := &http.Client{Timeout: 15 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return fiber.NewError(fiber.StatusInternalServerError, "Failed to call Python API")
	}
	defer resp.Body.Close()

	// 5. Relay response
	c.Status(resp.StatusCode)
	c.Set("Content-Type", resp.Header.Get("Content-Type"))
	_, copyErr := io.Copy(c, resp.Body)
	return copyErr
}
