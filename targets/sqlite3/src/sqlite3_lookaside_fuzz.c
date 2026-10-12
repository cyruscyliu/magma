#include <stddef.h>
#include <stdint.h>

#include "sqlite3.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  sqlite3 *db = 0;
  int slot_size;
  int slot_count;
  uint32_t encoded_size;

  if (size < 5) {
    return 0;
  }

  encoded_size = (uint32_t)data[0] |
                 ((uint32_t)data[1] << 8) |
                 ((uint32_t)data[2] << 16) |
                 ((uint32_t)data[3] << 24);
  slot_size = (int)(int32_t)encoded_size;
  slot_count = 1 + (data[4] & 0x7f);

  if (sqlite3_open(":memory:", &db) == SQLITE_OK) {
    sqlite3_db_config(db, SQLITE_DBCONFIG_LOOKASIDE, NULL, slot_size,
                      slot_count);
    sqlite3_exec(db, "CREATE TABLE lookaside_probe(x)", 0, 0, 0);
    sqlite3_close(db);
  }

  return 0;
}
