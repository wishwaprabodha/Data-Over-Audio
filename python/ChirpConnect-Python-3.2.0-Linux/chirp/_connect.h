/* ------------------------------------------------------------------------
 *
 *  This file is part of the Chirp Connect Python SDK.
 *  For full information on usage and licensing, see https://chirp.io/
 *
 *  Copyright (c) 2011-2018, Asio Ltd.
 *  All rights reserved.
 *
 * ------------------------------------------------------------------------ */

#ifndef __CONNECT_H__
#define __CONNECT_H__

/*************************************************************
 * Initialisation
 *************************************************************/
static PyObject *
connect_new_chirp_connect(PyObject *self, PyObject *args);
static PyObject *
connect_del_chirp_connect(PyObject *self, PyObject *args);

/*************************************************************
 * Getters & Setters
 *************************************************************/
static PyObject *
connect_chirp_connect_set_licence(PyObject *self, PyObject *args);

/*************************************************************
 * Processing
 *************************************************************/
static PyObject *
connect_chirp_connect_process_input(PyObject *self, PyObject *args);
static PyObject *
connect_chirp_connect_process_output(PyObject *self, PyObject *args);
static PyObject *
connect_chirp_connect_process_shorts_input(PyObject *self, PyObject *args);
static PyObject *
connect_chirp_connect_process_shorts_output(PyObject *self, PyObject *args);

#endif
