#include <cstdint>

#include "Object.h"
#include "PDFDoc.h"
#include "Stream.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    MemStream *stream = new MemStream(reinterpret_cast<const char *>(data), 0, static_cast<Goffset>(size), Object::null());
    PDFDoc doc(stream);
    if (!doc.isOk()) {
        return 0;
    }

    (void)doc.savePageAs("/dev/null", 1);
    return 0;
}
