#include <archive.h>
#include <archive_entry.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <locale.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

static int mkdir_p(const char *path) {
    char tmp[PATH_MAX];
    size_t len = strlen(path);
    if (len >= sizeof(tmp)) return -1;
    strcpy(tmp, path);
    if (len && tmp[len-1] == '/') tmp[len-1] = 0;
    for (char *p = tmp + 1; *p; p++) {
        if (*p == '/') { *p = 0; if (mkdir(tmp, 0755) && errno != EEXIST) return -1; *p = '/'; }
    }
    if (mkdir(tmp, 0755) && errno != EEXIST) return -1;
    return 0;
}

static const char *base_name(const char *p) {
    const char *s = strrchr(p, '/');
    const char *b = strrchr(p, '\\');
    if (!s || (b && b > s)) s = b;
    return s ? s + 1 : p;
}

int main(int argc, char **argv) {
    setlocale(LC_ALL, "C.UTF-8");
    if (argc != 3) { fprintf(stderr, "usage: %s archive outdir\n", argv[0]); return 2; }
    const char *src = argv[1], *out = argv[2];
    if (mkdir_p(out)) { perror("mkdir_p"); return 3; }
    struct archive *a = archive_read_new();
    archive_read_support_filter_all(a);
    archive_read_support_format_rar(a);
    archive_read_support_format_rar5(a);
    if (archive_read_open_filename(a, src, 10240) != ARCHIVE_OK) {
        fprintf(stderr, "open: %s\n", archive_error_string(a)); return 4;
    }
    struct archive_entry *entry;
    char buf[1<<16];
    int hr;
    while ((hr = archive_read_next_header(a, &entry)) == ARCHIVE_OK) {
        const char *bn = base_name(archive_entry_pathname(entry));
        if (!bn || !*bn || strstr(bn, "..")) { fprintf(stderr, "unsafe name\n"); return 5; }
        char dest[PATH_MAX];
        if (snprintf(dest, sizeof(dest), "%s/%s", out, bn) >= (int)sizeof(dest)) return 6;
        if (archive_entry_filetype(entry) == AE_IFDIR) { mkdir_p(dest); archive_read_data_skip(a); continue; }
        int fd = open(dest, O_WRONLY|O_CREAT|O_TRUNC, 0644);
        if (fd < 0) { perror("open dest"); return 7; }
        ssize_t n;
        while ((n = archive_read_data(a, buf, sizeof(buf))) > 0) {
            ssize_t off = 0;
            while (off < n) { ssize_t w = write(fd, buf + off, n - off); if (w < 0) { perror("write"); close(fd); return 8; } off += w; }
        }
        close(fd);
        if (n < 0) { fprintf(stderr, "read: %s\n", archive_error_string(a)); return 9; }
    }
    if (hr != ARCHIVE_EOF) { fprintf(stderr, "next_header status=%d err=%s\n", hr, archive_error_string(a)); archive_read_free(a); return 10; }
    archive_read_free(a);
    return 0;
}
