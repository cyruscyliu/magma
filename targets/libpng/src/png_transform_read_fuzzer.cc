#include <csetjmp>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <cstring>

#include "png.h"

namespace {

struct BufferState {
  const png_byte* data;
  size_t bytes_left;
};

void ReadData(png_structp png_ptr, png_bytep data, size_t length) {
  BufferState* state = static_cast<BufferState*>(png_get_io_ptr(png_ptr));
  if (length > state->bytes_left) {
    png_error(png_ptr, "unexpected end of PNG data");
  }
  memcpy(data, state->data, length);
  state->data += length;
  state->bytes_left -= length;
}

}  // namespace

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
  constexpr size_t signature_size = 8;
  if (size < signature_size || png_sig_cmp(data, 0, signature_size) != 0) {
    return 0;
  }

  png_structp png_ptr = png_create_read_struct(PNG_LIBPNG_VER_STRING, nullptr,
                                               nullptr, nullptr);
  if (png_ptr == nullptr) {
    return 0;
  }

  png_infop info_ptr = png_create_info_struct(png_ptr);
  png_infop end_info_ptr = png_create_info_struct(png_ptr);
  png_bytep row = nullptr;

  if (info_ptr == nullptr || end_info_ptr == nullptr) {
    png_destroy_read_struct(&png_ptr, info_ptr == nullptr ? nullptr : &info_ptr,
                            end_info_ptr == nullptr ? nullptr : &end_info_ptr);
    return 0;
  }

  if (setjmp(png_jmpbuf(png_ptr)) != 0) {
    free(row);
    png_destroy_read_struct(&png_ptr, &info_ptr, &end_info_ptr);
    return 0;
  }

  BufferState state{data + signature_size, size - signature_size};
  png_set_read_fn(png_ptr, &state, ReadData);
  png_set_sig_bytes(png_ptr, signature_size);
  png_set_crc_action(png_ptr, PNG_CRC_QUIET_USE, PNG_CRC_QUIET_USE);

  png_read_info(png_ptr, info_ptr);

  png_color_16 background;
  memset(&background, 0, sizeof(background));
  background.red = 255;
  background.green = 255;
  background.blue = 255;
  background.gray = 255;
  png_set_alpha_mode(png_ptr, PNG_ALPHA_OPTIMIZED, PNG_GAMMA_sRGB);
  png_set_background(png_ptr, &background, PNG_BACKGROUND_GAMMA_SCREEN, 0, 0);

  png_colorp palette = nullptr;
  int palette_size = 0;
  if (png_get_PLTE(png_ptr, info_ptr, &palette, &palette_size) != 0 &&
      palette != nullptr && palette_size > 0) {
    png_uint_16p histogram = nullptr;
    (void)png_get_hIST(png_ptr, info_ptr, &histogram);
    png_set_quantize(png_ptr, palette, palette_size, 16, histogram, 0);
  }

  png_read_update_info(png_ptr, info_ptr);

  const png_uint_32 height = png_get_image_height(png_ptr, info_ptr);
  const size_t row_size = png_get_rowbytes(png_ptr, info_ptr);
  row = static_cast<png_bytep>(malloc(row_size == 0 ? 1 : row_size));
  if (row == nullptr) {
    png_error(png_ptr, "row allocation failed");
  }

  for (png_uint_32 y = 0; y < height; ++y) {
    png_read_row(png_ptr, row, nullptr);
  }
  png_read_end(png_ptr, end_info_ptr);

  free(row);
  png_destroy_read_struct(&png_ptr, &info_ptr, &end_info_ptr);
  return 0;
}
