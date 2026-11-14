package main

import (
	"fmt"
	"io"
	"log"
	"os"

	"github.com/kkdai/youtube/v2"
)

func main() {
	videoID := "https://www.youtube.com/watch?v=RnFDSakZwac"
	if len(os.Args) > 1 {
		videoID = os.Args[1]
	}

	clients := []struct {
		name string
		info youtube.ClientInfo
	}{
		{"Android", youtube.AndroidClient},
		{"iOS", youtube.IOSClient},
		{"Web", youtube.WebClient},
		{"Embedded", youtube.EmbeddedClient},
	}

	var lastErr error
	for _, c := range clients {
		youtube.DefaultClient = c.info
		client := youtube.Client{
			MaxRoutines: 1, // avoid aggressive concurrent range requests
		}

		fmt.Printf("Trying %s client...\n", c.name)
		if err := tryDownload(&client, videoID, "tdk_lens_cleaner.mp4"); err != nil {
			log.Printf("%s client failed: %v", c.name, err)
			lastErr = err
			continue
		}

		fmt.Printf("Success using %s client!\n", c.name)
		return
	}

	log.Fatalf("all clients failed; last error: %v", lastErr)
}

func tryDownload(client *youtube.Client, videoID, outPath string) error {
	video, err := client.GetVideo(videoID)
	if err != nil {
		return fmt.Errorf("GetVideo: %w", err)
	}

	formats := video.Formats.WithAudioChannels()
	if len(formats) == 0 {
		return fmt.Errorf("no formats with audio channels found")
	}

	for _, f := range formats {
		stream, _, err := client.GetStream(video, &f)
		if err != nil {
			continue
		}

		file, err := os.Create(outPath)
		if err != nil {
			stream.Close()
			return err
		}

		written, copyErr := io.Copy(file, stream)
		stream.Close()
		file.Close()

		if copyErr == nil {
			fmt.Printf("Downloaded %q (itag=%d, quality=%s, %d bytes) to ./%s\n",
				video.Title, f.ItagNo, f.Quality, written, outPath)
			return nil
		}

		_ = os.Remove(outPath)
		log.Printf("itag %d (%s) failed: %v", f.ItagNo, f.Quality, copyErr)
	}

	return fmt.Errorf("all formats returned errors (likely 403)")
}
