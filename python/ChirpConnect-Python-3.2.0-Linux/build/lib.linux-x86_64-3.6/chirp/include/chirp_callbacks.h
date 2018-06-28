/**------------------------------------------------------------------------------
 *
 *  ASIO CONFIDENTIAL
 *
 *  @file chirp_callbacks.h
 *
 *  All contents are strictly proprietary, and not for copying, resale,
 *  or use outside of the agreed license.
 *
 *  Copyright © 2011-2018, Asio Ltd.
 *  All rights reserved.
 *
 *----------------------------------------------------------------------------*/

#ifndef __CHIRP_CONNECT_CALLBACK_H__
#define __CHIRP_CONNECT_CALLBACK_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "chirp_states.h"

typedef void (*chirp_connect_callback_t)(void *connect, uint8_t *bytes, size_t length);
typedef void (*chirp_connect_state_callback_t)(void *connect, chirp_connect_state_t old_state, chirp_connect_state_t new_state);

typedef struct _chirp_connect_callback_set_t {
    chirp_connect_state_callback_t on_state_changed;
    chirp_connect_callback_t on_sending;
    chirp_connect_callback_t on_sent;
    chirp_connect_callback_t on_receiving;
    chirp_connect_callback_t on_received;
} chirp_connect_callback_set_t;

#ifdef __cplusplus
}
#endif
#endif // __CHIRP_CONNECT_CALLBACK_H__
