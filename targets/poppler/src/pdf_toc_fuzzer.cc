#include <cstdint>
#include <string>

#include <poppler-document.h>
#include <poppler-toc.h>

static void nop_func(const std::string &message, void *data)
{
    (void)message;
    (void)data;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    poppler::set_debug_error_function(nop_func, nullptr);

    poppler::document *doc = poppler::document::load_from_raw_data(reinterpret_cast<const char *>(data), size);
    if (!doc || doc->is_locked()) {
        delete doc;
        return 0;
    }

    poppler::toc *document_toc = doc->create_toc();
    if (document_toc != nullptr) {
        (void)document_toc->root()->children();
        delete document_toc;
    }

    delete doc;
    return 0;
}
