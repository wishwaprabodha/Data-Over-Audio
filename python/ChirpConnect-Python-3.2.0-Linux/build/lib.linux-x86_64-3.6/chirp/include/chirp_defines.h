/**------------------------------------------------------------------------------
 *
 *  ASIO CONFIDENTIAL
 *
 *  @file chirp_defines.h
 *
 *  All contents are strictly proprietary, and not for copying, resale,
 *  or use outside of the agreed license.
 *
 *  Copyright © 2011-2018, Asio Ltd.
 *  All rights reserved.
 *
 *----------------------------------------------------------------------------*/

#ifndef __CHIRP_CONNECT_DEFINES_H__
#define __CHIRP_CONNECT_DEFINES_H__

#ifdef __cplusplus
extern "C" {
#endif

#if defined(__WIN32) || defined(_WIN32) || defined(WIN32)
#  define PUBLIC_SYM __declspec(dllexport)
#else
#  define PUBLIC_SYM __attribute__ ((visibility ("default")))
#endif

#define CHIRP_CONNECT_BUFFER_SIZE 4096

#ifdef __cplusplus
}
#endif
#endif // __CHIRP_CONNECT_DEFINES_H__
