// Package lib holds small query-building helpers shared by the handlers.
package lib

import (
	"fmt"
	"strings"
)

// WhereEquals renders a simple equality predicate.
func WhereEquals(field, value string) string {
	return fmt.Sprintf("%s = '%s'", field, value)
}

// Placeholders returns "?, ?, ?" with n markers.
func Placeholders(n int) string {
	if n <= 0 {
		return ""
	}
	return strings.TrimSuffix(strings.Repeat("?, ", n), ", ")
}

// Dollar returns "$1, $2, ..." starting at offset+1.
func Dollar(n, offset int) string {
	parts := make([]string, 0, n)
	for i := 1; i <= n; i++ {
		parts = append(parts, fmt.Sprintf("$%d", i+offset))
	}
	return strings.Join(parts, ", ")
}
