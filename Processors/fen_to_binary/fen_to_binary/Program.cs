using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.Runtime.InteropServices;

namespace fen_to_binary
{
    partial class Program
    {
        [SuppressGCTransition]
        [LibraryImport("/home/neo/Projects/Personal/chess_deep_learning/Processors/go/chesslib.so", StringMarshalling = StringMarshalling.Utf8)]
        private static partial IntPtr MarshalBinary(string fen);

        private static void AddBinaryColumnIfNotExists(SQLiteConnection db)
        {
            var checkColumnQuery = "PRAGMA table_info(evaluations)";
            var checkColumnCommand = new SQLiteCommand(checkColumnQuery, db);
            var columnReader = checkColumnCommand.ExecuteReader();

            var columnExists = false;

            while (columnReader.Read())
            {
                var columnName = columnReader["name"].ToString();
                if (columnName.Equals("binary", StringComparison.OrdinalIgnoreCase))
                {
                    columnExists = true;
                    break;
                }
            }

            if (!columnExists)
            {
                var addColumnQuery = "ALTER TABLE evaluations ADD COLUMN binary TEXT";
                var addColumnCommand = new SQLiteCommand(addColumnQuery, db);
                addColumnCommand.ExecuteNonQuery();
            }
        }

        private static void UpdateDatabaseBatch(SQLiteConnection db, List<(long id, string base64Position)> updates)
        {
            using (var transaction = db.BeginTransaction())
            {
                try
                {
                    var updateQuery = "UPDATE evaluations SET binary = @base64Position WHERE id = @id";
                    using (var updateCommand = new SQLiteCommand(updateQuery, db))
                    {
                        updateCommand.Parameters.Add("@base64Position", System.Data.DbType.String);
                        updateCommand.Parameters.Add("@id", System.Data.DbType.Int64);

                        foreach (var (id, base64Position) in updates)
                        {
                            updateCommand.Parameters["@base64Position"].Value = base64Position;
                            updateCommand.Parameters["@id"].Value = id;
                            updateCommand.ExecuteNonQuery();
                        }
                    }

                    transaction.Commit();
                }
                catch (Exception)
                {
                    transaction.Rollback();
                    throw;
                }
            }
        }

        static void Main(string[] args)
        {
            using (var db = new SQLiteConnection("Data Source=/home/neo/Projects/Personal/chess_deep_learning/dataset/chess_evals.db;Version=3;Pooling=true;Max Pool Size=100;"))
            {
                db.Open();
                AddBinaryColumnIfNotExists(db);

                var batchSize = 100000;
                var updates = new List<(long id, string base64Position)>();

                var totalRows = 0;
                var processedRows = 0;

                var query = $"SELECT * FROM evaluations WHERE binary is NULL";
                using (var command = new SQLiteCommand(query, db))
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        totalRows++;
                    }
                }

                Console.WriteLine($"Total rows to process: {totalRows}");

                while (processedRows < totalRows)
                {
                    var selectQuery = $"SELECT * FROM evaluations WHERE binary is NULL LIMIT {batchSize}";
                    using (var selectCommand = new SQLiteCommand(selectQuery, db))
                    using (var selectReader = selectCommand.ExecuteReader())
                    {
                        while (selectReader.Read())
                        {
                            var fen = selectReader["fen"].ToString();
                            var binary = MarshalBinary(fen);
                            var base64Position = Marshal.PtrToStringUTF8(binary);
                            var id = (long)selectReader["id"];

                            updates.Add((id, base64Position));

                            processedRows++;
                            Console.Write($"\rProcessed rows: {processedRows}/{totalRows}");

                            if (updates.Count == batchSize)
                            {
                                UpdateDatabaseBatch(db, updates);
                                updates.Clear();
                            }
                        }
                    }

                    if (updates.Count > 0)
                    {
                        UpdateDatabaseBatch(db, updates);
                        updates.Clear();
                    }
                }

                Console.WriteLine("\nProcessing complete!");
            }
        }
    }
}