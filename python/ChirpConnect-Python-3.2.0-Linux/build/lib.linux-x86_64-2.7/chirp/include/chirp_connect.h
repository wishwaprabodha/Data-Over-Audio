/**------------------------------------------------------------------------------
 *
 *  ASIO CONFIDENTIAL
 *
 *  @file chirp_connect.h
 *
 *  All contents are strictly proprietary, and not for copying, resale,
 *  or use outside of the agreed license.
 *
 *  Copyright © 2011-2018, Asio Ltd.
 *  All rights reserved.
 *
 *----------------------------------------------------------------------------*/

#ifndef __CHIRP_CONNECT_H__
#define __CHIRP_CONNECT_H__

#ifdef __cplusplus
extern "C" {
#endif

#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#include "chirp_callbacks.h"
#include "chirp_defines.h"
#include "chirp_errors.h"
#include "chirp_states.h"

// Typedef
typedef struct _chirp_connect_t chirp_connect_t;

// Utils
PUBLIC_SYM void chirp_connect_trigger_callbacks(chirp_connect_t *ca, uint8_t *bytes, size_t length);
PUBLIC_SYM char *chirp_connect_get_info(chirp_connect_t *ca);

// Ctor & Dtor
PUBLIC_SYM chirp_connect_t *new_chirp_connect(const char *key, const char *secret);
PUBLIC_SYM chirp_connect_error_code_t del_chirp_connect(chirp_connect_t* ca);

// Getters & Setters
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_set_licence(chirp_connect_t *ca, const char *licence);
PUBLIC_SYM void chirp_connect_set_random_seed(chirp_connect_t *ca, uint32_t seed);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_set_volume(chirp_connect_t *ca, float volume);
PUBLIC_SYM float chirp_connect_get_volume(chirp_connect_t *ca);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_set_sample_rate(chirp_connect_t *ca, uint32_t sample_rate);
PUBLIC_SYM uint32_t chirp_connect_get_sample_rate(chirp_connect_t *ca);
PUBLIC_SYM chirp_connect_state_t chirp_connect_get_state(chirp_connect_t *ca);
PUBLIC_SYM void chirp_connect_set_auto_mute(chirp_connect_t *ca, bool auto_mute);
PUBLIC_SYM bool chirp_connect_get_auto_mute(chirp_connect_t *ca);
PUBLIC_SYM const char *chirp_connect_get_protocol_name(chirp_connect_t *ca);
PUBLIC_SYM float chirp_connect_get_duration_for_payload_length(chirp_connect_t *ca, size_t length);
PUBLIC_SYM uint8_t chirp_connect_get_protocol_version(chirp_connect_t *ca);
PUBLIC_SYM time_t chirp_connect_get_expiry_time(chirp_connect_t *ca);

// States
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_start(chirp_connect_t *ca);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_pause(chirp_connect_t *ca, bool pause);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_stop(chirp_connect_t *ca);

// Callbacks
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_set_callbacks(chirp_connect_t *ca, chirp_connect_callback_set_t callbacks);
PUBLIC_SYM void chirp_connect_set_callback_ptr(chirp_connect_t *ca, void *ptr);

// Processing
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_process(chirp_connect_t *ca, float *in, float *out, size_t size);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_process_input(chirp_connect_t *ca, float *buffer, size_t size);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_process_output(chirp_connect_t *ca, float *buffer, size_t size);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_process_shorts(chirp_connect_t *ca, short *in, short *out, size_t size);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_process_shorts_input(chirp_connect_t *ca, const short *buffer, size_t size);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_process_shorts_output(chirp_connect_t *ca, short *buffer, size_t size);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_process_playthrough(chirp_connect_t *ca, size_t size);

// Payload
PUBLIC_SYM size_t chirp_connect_get_max_payload_length(chirp_connect_t *ca);
PUBLIC_SYM uint8_t *chirp_connect_new_payload(chirp_connect_t *ca, size_t length);
PUBLIC_SYM uint8_t *chirp_connect_random_payload(chirp_connect_t *ca, size_t length);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_is_valid(chirp_connect_t *ca, const uint8_t *bytes, size_t length);
PUBLIC_SYM char *chirp_connect_as_string(chirp_connect_t *ca, uint8_t *bytes, size_t length);
PUBLIC_SYM chirp_connect_error_code_t chirp_connect_send(chirp_connect_t *ca, uint8_t *bytes, size_t length);

#ifdef __cplusplus
}
#endif
#endif // __CHIRP_CONNECT_H__
