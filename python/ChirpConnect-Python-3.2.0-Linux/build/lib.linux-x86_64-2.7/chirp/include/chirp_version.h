/**------------------------------------------------------------------------------
 *
 *  ASIO CONFIDENTIAL
 *
 *  @file chirp_version.h
 *
 *  All contents are strictly proprietary, and not for copying, resale,
 *  or use outside of the agreed license.
 *
 *  Copyright © 2011-2018, Asio Ltd.
 *  All rights reserved.
 *
 *----------------------------------------------------------------------------*/

#ifndef __CHIRP_CONNECT_VERSION_H__
#define __CHIRP_CONNECT_VERSION_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "chirp_defines.h"

typedef struct _chirp_package_t {
    const char *name;
    const char *version;
    const char *build;
} chirp_package_t;

typedef struct _chirp_version_t {
    chirp_package_t connect;
    chirp_package_t engine;
    chirp_package_t crypto;
} chirp_version_t;

PUBLIC_SYM chirp_version_t chirp_connect_get_version(void);
PUBLIC_SYM const char *chirp_connect_get_package_full_version(void);
PUBLIC_SYM const char *chirp_connect_get_package_name(void);
PUBLIC_SYM const char *chirp_connect_get_package_version(void);
PUBLIC_SYM const char *chirp_connect_get_package_build(void);

#ifdef __cplusplus
}
#endif
#endif // __CHIRP_CONNECT_VERSION_H__
