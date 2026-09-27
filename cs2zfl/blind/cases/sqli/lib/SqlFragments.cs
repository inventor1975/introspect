using System.Collections.Generic;
using Microsoft.Data.SqlClient;

namespace Storefront.Data
{
    public static class SqlFragments
    {
        public static string WhereEquals(string column, string value)
        {
            return " WHERE " + column + " = '" + value + "'";
        }

        public static string Literal(string value)
        {
            if (value == null)
            {
                return "NULL";
            }
            return "N'" + value.Trim() + "'";
        }

        public static string BindEquals(SqlCommand command, string column, object value)
        {
            var name = "@p" + command.Parameters.Count;
            command.Parameters.AddWithValue(name, value);
            return column + " = " + name;
        }

        public static string BindList(SqlCommand command, IEnumerable<string> values)
        {
            var names = new List<string>();
            foreach (var v in values)
            {
                var name = "@v" + command.Parameters.Count;
                command.Parameters.AddWithValue(name, v);
                names.Add(name);
            }
            return string.Join(", ", names);
        }
    }
}
