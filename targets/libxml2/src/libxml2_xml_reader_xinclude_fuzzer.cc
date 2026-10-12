#include <cstddef>
#include <cstdint>

#include "libxml/xmlreader.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  xmlTextReaderPtr reader = xmlReaderForMemory(
      reinterpret_cast<const char *>(data),
      static_cast<int>(size),
      "instance.xml",
      nullptr,
      XML_PARSE_XINCLUDE | XML_PARSE_DTDVALID);
  if (reader == nullptr)
    return 0;

  while (xmlTextReaderRead(reader) == 1) {
    xmlTextReaderNodeType(reader);
    xmlTextReaderConstValue(reader);
  }

  xmlFreeTextReader(reader);
  return 0;
}
