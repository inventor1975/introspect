package blind2.xss.spring;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PagingController {

    @GetMapping(value = "/members/pager", produces = "text/html")
    public String pager(@RequestParam(value = "page", defaultValue = "1") int page,
                        @RequestParam(value = "sort", defaultValue = "name") String sort) {
        String column;
        switch (sort) {
            case "joined":
                column = "joined";
                break;
            case "posts":
                column = "posts";
                break;
            default:
                column = "name";
        }
        int prev = Math.max(1, page - 1);
        return "<nav class=\"pager\"><a href=\"?page=" + prev + "&sort=" + column + "\">&laquo;</a>"
                + "<span>Page " + page + " sorted by " + column + "</span>"
                + "<a href=\"?page=" + (page + 1) + "&sort=" + column + "\">&raquo;</a></nav>";
    }
}
