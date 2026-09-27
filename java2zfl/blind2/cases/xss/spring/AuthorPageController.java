package blind2.xss.spring;

import blind2.xss.support.AuthorRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@RestController
public class AuthorPageController {

    private final AuthorRepository authors;

    public AuthorPageController(AuthorRepository authors) {
        this.authors = authors;
    }

    @GetMapping(value = "/authors/{id}", produces = "text/html")
    public String author(@PathVariable("id") long id) {
        String name = authors.findDisplayName(id);
        String bio = authors.findBio(id);
        return "<article><h1>" + HtmlUtils.htmlEscape(name) + "</h1>"
                + "<section class=\"bio\">" + bio + "</section></article>";
    }
}
