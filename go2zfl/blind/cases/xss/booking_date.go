package bookingdate

import (
	"fmt"
	"net/http"
	"time"
)

func BookingSummary(w http.ResponseWriter, r *http.Request) {
	checkIn, err := time.Parse("2006-01-02", r.FormValue("checkin"))
	if err != nil {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		fmt.Fprint(w, "<p class=\"error\">Please pick a valid check-in date.</p>")
		return
	}
	nights := 3
	checkOut := checkIn.AddDate(0, 0, nights)

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<p>Check-in: %s<br>Check-out: %s</p>",
		checkIn.Format("Mon, 02 Jan 2006"), checkOut.Format("Mon, 02 Jan 2006"))
}
