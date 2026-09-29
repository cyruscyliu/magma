#include <cstddef>
#include <cstdint>

#include "libxml/parser.h"
#include "libxml/xmlschemas.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  if (size < 4)
    return 0;

  size_t schemaSize = static_cast<size_t>(data[0]) |
                      (static_cast<size_t>(data[1]) << 8) |
                      (static_cast<size_t>(data[2]) << 16) |
                      (static_cast<size_t>(data[3]) << 24);
  size_t remaining = size - 4;
  if (schemaSize == 0 || schemaSize > remaining)
    return 0;

  const char *schemaData = reinterpret_cast<const char *>(data + 4);
  const char *documentData = reinterpret_cast<const char *>(data + 4 + schemaSize);
  size_t documentSize = remaining - schemaSize;

  xmlSchemaParserCtxtPtr parserContext =
      xmlSchemaNewMemParserCtxt(schemaData, static_cast<int>(schemaSize));
  if (parserContext == nullptr)
    return 0;

  xmlSchemaPtr schema = xmlSchemaParse(parserContext);
  xmlSchemaFreeParserCtxt(parserContext);
  if (schema == nullptr)
    return 0;

  xmlDocPtr document = xmlReadMemory(documentData,
                                     static_cast<int>(documentSize),
                                     "instance.xml",
                                     nullptr,
                                     0);
  if (document != nullptr) {
    xmlSchemaValidCtxtPtr validContext = xmlSchemaNewValidCtxt(schema);
    if (validContext != nullptr) {
      xmlSchemaValidateDoc(validContext, document);
      xmlSchemaFreeValidCtxt(validContext);
    }
    xmlFreeDoc(document);
  }

  xmlSchemaFree(schema);
  return 0;
}
