using System.Text;

namespace Storefront.Data
{
    public class ReportFilter
    {
        public string Status { get; set; } = "";
        public string CustomerName { get; set; } = "";
        public int? MinTotal { get; set; }

        public string ToWhereClause()
        {
            var sb = new StringBuilder(" WHERE 1=1");
            if (!string.IsNullOrEmpty(Status))
            {
                sb.Append(" AND o.Status = '").Append(Status).Append('\'');
            }
            if (!string.IsNullOrEmpty(CustomerName))
            {
                sb.Append(" AND c.Name LIKE '%").Append(CustomerName).Append("%'");
            }
            if (MinTotal.HasValue)
            {
                sb.Append(" AND o.Total >= ").Append(MinTotal.Value);
            }
            return sb.ToString();
        }
    }
}
