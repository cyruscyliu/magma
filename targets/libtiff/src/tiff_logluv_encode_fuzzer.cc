#include <cstddef>
#include <cstdint>
#include <cstring>
#include <sstream>
#include <tiffio.h>
#include <tiffio.hxx>

extern "C" void handle_error(const char *, const char *, va_list) {}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    constexpr size_t kMaxBytes = 1024 * 1024;
    constexpr size_t kBytesPerPixel = 3 * sizeof(float);
    if (size < kBytesPerPixel || size > kMaxBytes) {
        return 0;
    }

    const size_t pixel_count = size / kBytesPerPixel;
    const size_t strip_size = pixel_count * kBytesPerPixel;
    std::ostringstream output;
    TIFF *tif = TIFFStreamOpen("MemTIFFOut", &output);
    if (tif == nullptr) {
        return 0;
    }

    TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, 1);
    TIFFSetField(tif, TIFFTAG_IMAGELENGTH,
                 static_cast<uint32_t>(pixel_count));
    TIFFSetField(tif, TIFFTAG_COMPRESSION, COMPRESSION_SGILOG24);
    TIFFSetField(tif, TIFFTAG_PHOTOMETRIC, PHOTOMETRIC_LOGLUV);
    TIFFSetField(tif, TIFFTAG_ROWSPERSTRIP,
                 static_cast<uint32_t>(pixel_count));
    TIFFSetField(tif, TIFFTAG_SGILOGDATAFMT, SGILOGDATAFMT_FLOAT);
    TIFFSetField(tif, TIFFTAG_SGILOGENCODE, SGILOGENCODE_NODITHER);

    TIFFWriteEncodedStrip(tif, 0, const_cast<void *>(
                                      static_cast<const void *>(data)),
                          static_cast<tmsize_t>(strip_size));
    TIFFClose(tif);
    return 0;
}
