package blind2.sqli;

import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AppointmentController {

    record SlotQuery(String doctorCode, String day) {
    }

    private final JdbcTemplate jdbc;

    public AppointmentController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/appointments/free")
    public List<String> freeSlots(@RequestParam String doctor, @RequestParam String day) {
        SlotQuery query = new SlotQuery(doctor.trim(), day);
        return jdbc.queryForList(toSql(query), String.class);
    }

    private static String toSql(SlotQuery q) {
        return "SELECT to_char(slot_start, 'HH24:MI') FROM slots WHERE doctor_code = '" + q.doctorCode()
                + "' AND slot_date = '" + q.day() + "' AND booked = false ORDER BY slot_start";
    }
}
