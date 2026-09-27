using System;
using System.IO;
using Microsoft.AspNetCore.Mvc;

public class FilesController : ControllerBase
{
    private static readonly string Root = Path.GetFullPath("/srv/files") + Path.DirectorySeparatorChar;

    public IActionResult Get([FromQuery] string path, [FromQuery] string name)
    {
        var full = Path.GetFullPath(Path.Combine(Root, path));
        if (!full.StartsWith(Root, StringComparison.Ordinal)) return Forbid();
        System.IO.File.ReadAllText(full);
        if (name.Contains("..")) return BadRequest();                  // an absolute path still replaces the base
        return PhysicalFile(Path.Combine("/srv/files", name), "application/octet-stream");
    }
}
