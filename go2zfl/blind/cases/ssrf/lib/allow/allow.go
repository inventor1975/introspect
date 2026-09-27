package allow

import (
	"errors"
	"net/url"
	"strings"
)

var trustedHosts = map[string]bool{
	"assets.acme-cdn.net": true,
	"images.acme-cdn.net": true,
	"static.partner.io":   true,
}

var ErrHost = errors.New("host not permitted")

// Check parses raw and returns it only if it is an https URL on a trusted host.
func Check(raw string) (*url.URL, error) {
	u, err := url.Parse(raw)
	if err != nil {
		return nil, err
	}
	if u.Scheme != "https" || u.User != nil {
		return nil, ErrHost
	}
	if !trustedHosts[strings.ToLower(u.Hostname())] {
		return nil, ErrHost
	}
	if p := u.Port(); p != "" && p != "443" {
		return nil, ErrHost
	}
	return u, nil
}
