using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Game.Launcher.Controllers
{
    [ApiController]
    [Route("api/translations")]
    public class TranslationFilesController : ControllerBase
    {
        private const string LangDir = "/app/launcher/lang";

        [HttpGet]
        public IActionResult Get([FromQuery] string lang)
        {
            string file;
            if (lang == "de")
            {
                file = "de.json";
            }
            else if (lang == "fr")
            {
                file = "fr.json";
            }
            else if (lang == "ja")
            {
                file = "ja.json";
            }
            else
            {
                file = "en.json";
            }

            var json = System.IO.File.ReadAllText(Path.Combine(LangDir, file));
            return Content(json, "application/json");
        }
    }
}
