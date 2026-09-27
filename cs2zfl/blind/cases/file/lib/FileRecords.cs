using System;
using Microsoft.EntityFrameworkCore;

namespace Shared.Storage
{
    public class FileRecord
    {
        public int Id { get; set; }
        public string OwnerId { get; set; } = "";
        public string OriginalName { get; set; } = "";
        public string StoragePath { get; set; } = "";
        public long Size { get; set; }
        public DateTime UploadedUtc { get; set; }
    }

    public class FilesDbContext : DbContext
    {
        public FilesDbContext(DbContextOptions<FilesDbContext> options) : base(options) { }

        public DbSet<FileRecord> Files => Set<FileRecord>();
    }
}
