#include <algorithm>
#include <cstdarg>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <sstream>
#include <tiffio.h>
#include <tiffio.hxx>

namespace {

uint32_t read_le32(const uint8_t *data) {
    return static_cast<uint32_t>(data[0]) |
           (static_cast<uint32_t>(data[1]) << 8) |
           (static_cast<uint32_t>(data[2]) << 16) |
           (static_cast<uint32_t>(data[3]) << 24);
}

uint32_t aligned_control(uint32_t control, uint32_t granularity) {
    if (granularity == 0) {
        return 0;
    }
    const uint64_t scaled =
        static_cast<uint64_t>(granularity) * (1U + (control & 0xffffU));
    return static_cast<uint32_t>(std::min<uint64_t>(scaled, UINT32_MAX));
}

} // namespace

extern "C" void handle_region_error(const char *, const char *, va_list) {}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) {
        return 0;
    }

    const size_t payload_size = size - 8;
    const uint32_t requested_col = read_le32(data + payload_size);
    const uint32_t requested_row = read_le32(data + payload_size + 4);

    std::istringstream stream(std::string(data, data + payload_size));
    TIFF *tif = TIFFStreamOpen("MemTIFF", &stream);
    if (tif == nullptr) {
        return 0;
    }

    TIFFSetErrorHandler(handle_region_error);
    TIFFSetWarningHandler(handle_region_error);

    uint32_t raster_width = 0;
    uint32_t raster_height = 0;
    uint32_t col = 0;
    uint32_t row = 0;
    const bool tiled = TIFFIsTiled(tif) != 0;

    if (tiled) {
        uint32_t tile_width = 0;
        uint32_t tile_height = 0;
        if (!TIFFGetField(tif, TIFFTAG_TILEWIDTH, &tile_width) ||
            !TIFFGetField(tif, TIFFTAG_TILELENGTH, &tile_height)) {
            TIFFClose(tif);
            return 0;
        }
        raster_width = tile_width;
        raster_height = tile_height;
        col = aligned_control(requested_col, tile_width);
        row = aligned_control(requested_row, tile_height);
    } else {
        uint32_t width = 0;
        uint32_t rows_per_strip = 0;
        if (!TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width)) {
            TIFFClose(tif);
            return 0;
        }
        TIFFGetFieldDefaulted(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip);
        if (rows_per_strip == 0) {
            TIFFClose(tif);
            return 0;
        }
        raster_width = width;
        raster_height = rows_per_strip;
        row = aligned_control(requested_row, rows_per_strip);
    }

    const uint64_t raster_pixels =
        static_cast<uint64_t>(raster_width) * raster_height;
    if (raster_width == 0 || raster_height == 0 || raster_pixels > 1000000) {
        TIFFClose(tif);
        return 0;
    }

    uint32_t *raster = static_cast<uint32_t *>(
        _TIFFmalloc(static_cast<tmsize_t>(raster_pixels) * sizeof(uint32_t)));
    if (raster != nullptr) {
        if (tiled) {
            TIFFReadRGBATile(tif, col, row, raster);
        } else {
            TIFFReadRGBAStrip(tif, row, raster);
        }
        _TIFFfree(raster);
    }

    TIFFClose(tif);
    return 0;
}
