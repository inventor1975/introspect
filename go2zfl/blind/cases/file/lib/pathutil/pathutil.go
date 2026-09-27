// Package pathutil holds small helpers shared by the document portal handlers.
package pathutil

import (
	"errors"
	"os"
	"path/filepath"
	"strings"
)

// ErrOutsideBase is returned when a requested name resolves outside its base directory.
var ErrOutsideBase = errors.New("pathutil: path escapes base directory")

// Under returns the location of name inside base.
func Under(base, name string) string {
	return filepath.Join(base, name)
}

// Normalize makes user supplied names comparable: trims blanks and lowercases.
func Normalize(name string) string {
	name = strings.TrimSpace(name)
	name = strings.ToLower(name)
	return strings.Trim(name, " \t")
}

// Contained joins base and name and verifies the result stays inside base.
func Contained(base, name string) (string, error) {
	absBase, err := filepath.Abs(base)
	if err != nil {
		return "", err
	}
	full := filepath.Join(absBase, name)
	rel, err := filepath.Rel(absBase, full)
	if err != nil {
		return "", err
	}
	if rel == ".." || strings.HasPrefix(rel, ".."+string(os.PathSeparator)) || filepath.IsAbs(rel) {
		return "", ErrOutsideBase
	}
	return full, nil
}
