using System.IO;

namespace Shared.Storage
{
    public interface IAssetLocator
    {
        string Locate(string assetKey);
    }

    public class DiskAssetLocator : IAssetLocator
    {
        private readonly string _assetRoot;

        public DiskAssetLocator(string assetRoot)
        {
            _assetRoot = assetRoot;
        }

        public string Locate(string assetKey)
        {
            return Path.Combine(_assetRoot, assetKey);
        }
    }
}
