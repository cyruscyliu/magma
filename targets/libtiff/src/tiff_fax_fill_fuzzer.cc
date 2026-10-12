#include <algorithm>
#include <cstdint>
#include <cstring>
#include <sstream>
#include <tiffio.h>
#include <tiffio.hxx>

extern "C" void handle_error(const char *, const char *, va_list) {}

extern "C" void fax_fill(unsigned char *, uint32_t *, uint32_t, uint32_t) {}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
#ifndef STANDALONE
    TIFFSetErrorHandler(handle_error);
    TIFFSetWarningHandler(handle_error);
#endif

    std::istringstream stream(std::string(data, data + size));
    TIFF *tif = TIFFStreamOpen("MemTIFF", &stream);
    if (tif == nullptr) {
        return 0;
    }

    TIFFSetField(tif, TIFFTAG_FAXFILLFUNC, fax_fill);
    const uint32_t strip_count =
        std::min<uint32_t>(TIFFNumberOfStrips(tif), 1024);
    for (uint32_t strip = 0; strip < strip_count; ++strip) {
        TIFFReadEncodedStrip(tif, strip, nullptr, static_cast<tmsize_t>(-1));
    }

    TIFFClose(tif);
    return 0;
}
