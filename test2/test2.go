package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/lrstanley/go-ytdlp"
)

func main() {
	if len(os.Args) < 2 {
		log.Fatalf("usage: %s <youtube-url>", os.Args[0])
	}
	url := os.Args[1]
	ctx := context.Background()

	// Automatically downloads & caches yt-dlp if it isn't installed yet
	ytdlp.MustInstall(ctx, nil)

	dl := ytdlp.New().
		NoPlaylist().
		FormatSort("res,ext:mp4:m4a").
		RecodeVideo("mp4").
		Output("%(title)s.%(ext)s").
		ProgressFunc(250*time.Millisecond, func(prog ytdlp.ProgressUpdate) {
			fmt.Printf("\r[%s] %s (ETA: %s) -> %s",
				prog.Status,
				prog.PercentString(),
				prog.ETA().Round(time.Second),
				prog.Filename,
			)
		})

	// Want audio-only instead of MP4? Replace FormatSort/RecodeVideo above with:
	// Format("bestaudio/best").
	// ExtractAudio().
	// AudioFormat("mp3"). // or "m4a" / "opus"

	fmt.Println("Starting download...")
	_, err := dl.Run(ctx, url)
	fmt.Println() // newline after \r progress updates

	if err != nil {
		log.Fatalf("download failed: %v", err)
	}
	fmt.Println("Done!")
}
