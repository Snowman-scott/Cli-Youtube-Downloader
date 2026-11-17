package main

import (
	"bufio"
	"fmt"
	"io"
	"os/exec"
	"runtime"
	"strings"
)

func ClearTerminal() {
	var cmd *exec.Cmd
	if runtime.GOOS == "windows" {
		cmd = exec.Command("cls")
	} else {
		cmd = exec.Command("clear")
	}
	cmd.Run()
}

func ScannerHelper(prompt string, scanner *bufio.Scanner) (string, error) {
	fmt.Print(prompt)
	if !scanner.Scan() {
		if err := scanner.Err(); err != nil {
			return "", err
		}
		return "", io.EOF
	}
	return strings.TrimSpace(scanner.Text()), nil
}

func GetBrowserChoice() string {
	browserMap := map[string]string{
		"1": "chrome",
		"2": "firefox",
		"3": "edge",
		"4": "safari",
		"5": "",
	}
	fmt.Println("To Avoid Bot Detection, we will use your browsers cookies.\nWhich browser are you using?")
	for // code the for loop
}
