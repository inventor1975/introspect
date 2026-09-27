// Package pagekit holds small HTML building helpers shared by the site handlers.
package pagekit

import (
	"html"
	"strings"
)

// Escape makes a string safe for HTML text and quoted attribute values.
func Escape(s string) string {
	return html.EscapeString(s)
}

// StripAngles removes angle brackets so that no tags can be opened.
func StripAngles(s string) string {
	s = strings.ReplaceAll(s, "<", "")
	s = strings.ReplaceAll(s, ">", "")
	return s
}

// Card renders a titled panel.
func Card(title, body string) string {
	var b strings.Builder
	b.WriteString(`<section class="card">`)
	b.WriteString("<h2>" + title + "</h2>")
	b.WriteString("<div class=\"card-body\">" + body + "</div>")
	b.WriteString("</section>")
	return b.String()
}

// Layout wraps a fragment in the standard page chrome.
func Layout(title, content string) string {
	return "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>" +
		html.EscapeString(title) + "</title></head><body>" + content + "</body></html>"
}

// Truncate shortens s to at most n bytes.
func Truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
}
