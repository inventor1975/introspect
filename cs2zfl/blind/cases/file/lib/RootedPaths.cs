using System;
using System.IO;

namespace Shared.Storage
{
    public static class RootedPaths
    {
        public static string ResolveUnder(string root, string relative)
        {
            var rootFull = Path.GetFullPath(root);
            if (!rootFull.EndsWith(Path.DirectorySeparatorChar))
            {
                rootFull += Path.DirectorySeparatorChar;
            }

            var candidate = Path.GetFullPath(Path.Combine(rootFull, relative));
            if (!candidate.StartsWith(rootFull, StringComparison.Ordinal))
            {
                throw new UnauthorizedAccessException("Path escapes the storage root.");
            }

            return candidate;
        }
    }
}
