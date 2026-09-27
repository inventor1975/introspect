using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

public static class Endpoints
{
    public static void Map(WebApplication app)
    {
        app.MapGet("/greet", (string name) => Results.Content("<p>" + name + "</p>", "text/html"));
        app.MapGet("/order/{id:long}", (long id) => Results.Content("<p>" + id + "</p>", "text/html"));   // a number
        app.MapPost("/note", async (HttpRequest req) =>
        {
            var form = await req.ReadFormAsync();
            System.IO.File.WriteAllText("/srv/notes/" + form["file"], "x");
        });
    }
}
