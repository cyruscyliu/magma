#include <cstddef>
#include <cstdint>
#include <cstring>
#include <vector>

#include "png.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
  constexpr size_t signature_size = 8;
  if (size < signature_size || png_sig_cmp(data, 0, signature_size) != 0) {
    return 0;
  }

  png_image image;
  memset(&image, 0, sizeof(image));
  image.version = PNG_IMAGE_VERSION;

  if (png_image_begin_read_from_memory(&image, data, size) == 0) {
    return 0;
  }

  image.format = PNG_FORMAT_RGB;
  std::vector<png_byte> buffer(PNG_IMAGE_SIZE(image));
  (void)png_image_finish_read(&image, nullptr, buffer.data(), 0, nullptr);
  return 0;
}
