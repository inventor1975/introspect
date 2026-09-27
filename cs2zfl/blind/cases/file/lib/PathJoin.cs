namespace Shared.Storage
{
    public static class PathJoin
    {
        public static string UnderContent(string contentRoot, string relative)
        {
            var trimmed = relative.TrimStart('/');
            return contentRoot.TrimEnd('/') + "/" + trimmed;
        }
    }
}
