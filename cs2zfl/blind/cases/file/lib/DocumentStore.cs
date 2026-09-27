using System.IO;

namespace Shared.Storage
{
    public class DocumentStore
    {
        private readonly string _root;

        public DocumentStore(string root)
        {
            _root = root;
        }

        public bool Exists(string name)
        {
            return File.Exists(Path.Combine(_root, name));
        }

        public byte[] Load(string name)
        {
            var full = Path.Combine(_root, name);
            return File.ReadAllBytes(full);
        }
    }
}
