using System;
using System.Globalization;
using System.IO;

namespace Shared.Storage
{
    public class ThumbnailCache
    {
        private readonly string _cacheDir;

        public ThumbnailCache(string cacheDir)
        {
            _cacheDir = cacheDir;
        }

        public string PathFor(Guid imageId, int width, int height)
        {
            var name = string.Format(CultureInfo.InvariantCulture, "{0:N}_{1}x{2}.webp", imageId, width, height);
            return Path.Combine(_cacheDir, name);
        }
    }
}
