package blind2.sqli.support;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;

@Component
public class RegionInterceptor {

    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String region = request.getHeader("X-Sales-Region");
        ReportContext.setRegion(region != null ? region : "GLOBAL");
        return true;
    }

    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        ReportContext.clear();
    }
}
