/* ------------------------------------------------------------------------
 *
 *  This file is part of the Chirp Connect Python SDK.
 *  For full information on usage and licensing, see https://chirp.io/
 *
 *  Copyright (c) 2011-2018, Asio Ltd.
 *  All rights reserved.
 *
 * ------------------------------------------------------------------------ */

#include <Python.h>
#include "include/chirp_connect.h"
#include "include/chirp_errors.h"
#include "_connect.h"


/************************************************************
 * Python Methods
 ************************************************************/

static PyMethodDef connect_methods[] = {

    {
        "new_chirp_connect",
        connect_new_chirp_connect, METH_VARARGS,
        "initialise chirp connect"
    },
    {
        "del_chirp_connect",
        connect_del_chirp_connect, METH_VARARGS,
        "clean up chirp connect"
    },
    {
        "chirp_connect_set_licence",
        connect_chirp_connect_set_licence, METH_VARARGS,
        "set the licence string"
    },
    {
        "chirp_connect_process_input",
        connect_chirp_connect_process_input, METH_VARARGS,
        "process input audio data"
    },
    {
        "chirp_connect_process_output",
        connect_chirp_connect_process_output, METH_VARARGS,
        "process output audio data"
    },
    {
        "chirp_connect_process_shorts_input",
        connect_chirp_connect_process_shorts_input, METH_VARARGS,
        "process input audio data as shorts"
    },
    {
        "chirp_connect_process_shorts_output",
        connect_chirp_connect_process_shorts_output, METH_VARARGS,
        "process output audio data as shorts"
    },

    {NULL, NULL, 0, NULL}
};

static PyObject *ConnectError;
static chirp_connect_t *ca;

/*************************************************************
 * Initialisation
 *************************************************************/

static PyObject *
connect_new_chirp_connect(PyObject *self, PyObject *args)
{
    const char *key;
    const char *secret;

    if (!PyArg_ParseTuple(args, "ss", &key, &secret))
        return NULL;

    ca = new_chirp_connect(key, secret);
    if (!ca) {
        PyErr_SetString(ConnectError, "Failed to initialise Chirp Connect");
        return NULL;
    }

    return PyLong_FromVoidPtr(ca);
}

static PyObject *
connect_del_chirp_connect(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    chirp_connect_error_code_t err = del_chirp_connect(ca);
    if (err != CHIRP_CONNECT_OK) {
        PyErr_SetString(ConnectError, chirp_connect_error_code_to_string(err));
        return NULL;
    }
    Py_RETURN_NONE;
}

/*************************************************************
 * Getters & Setters
 *************************************************************/

static PyObject *
connect_chirp_connect_set_licence(PyObject *self, PyObject *args)
{
    const char *licence;

    if (!PyArg_ParseTuple(args, "s", &licence))
        return NULL;

    chirp_connect_error_code_t err = chirp_connect_set_licence(ca, licence);
    if (err != CHIRP_CONNECT_OK) {
        PyErr_SetString(ConnectError, chirp_connect_error_code_to_string(err));
        return NULL;
    }
    Py_RETURN_NONE;
}

/*************************************************************
 * Processing
 *************************************************************/

static PyObject *
connect_chirp_connect_process_input(PyObject *self, PyObject *args)
{
    char *data;
    int length;
    float *buffer;

    if (!PyArg_ParseTuple(args, "s#", &data, &length))
        return NULL;

    buffer = (float *)data;

    chirp_connect_error_code_t err = chirp_connect_process_input(ca, buffer, (length / 4));
    if (err != CHIRP_CONNECT_OK) {
        PyErr_SetString(ConnectError, chirp_connect_error_code_to_string(err));
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *
connect_chirp_connect_process_output(PyObject *self, PyObject *args)
{
    char *data;
    int length;
    float *buffer;

    if (!PyArg_ParseTuple(args, "s#", &data, &length))
        return NULL;

    buffer = (float *)data;

    chirp_connect_error_code_t err = chirp_connect_process_output(ca, buffer, (length / 4));
    if (err != CHIRP_CONNECT_OK) {
        PyErr_SetString(ConnectError, chirp_connect_error_code_to_string(err));
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *
connect_chirp_connect_process_shorts_input(PyObject *self, PyObject *args)
{
    char *data;
    int length;
    short *buffer;

    if (!PyArg_ParseTuple(args, "s#", &data, &length))
        return NULL;

    buffer = (short *)data;

    chirp_connect_error_code_t err = chirp_connect_process_shorts_input(ca, buffer, (length / 2));
    if (err != CHIRP_CONNECT_OK) {
        PyErr_SetString(ConnectError, chirp_connect_error_code_to_string(err));
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *
connect_chirp_connect_process_shorts_output(PyObject *self, PyObject *args)
{
    char *data;
    int length;
    short *buffer;

    if (!PyArg_ParseTuple(args, "s#", &data, &length))
        return NULL;

    buffer = (short *)data;

    chirp_connect_error_code_t err = chirp_connect_process_shorts_output(ca, buffer, (length / 2));
    if (err != CHIRP_CONNECT_OK) {
        PyErr_SetString(ConnectError, chirp_connect_error_code_to_string(err));
        return NULL;
    }
    Py_RETURN_NONE;
}


#if PY_MAJOR_VERSION >= 3
#define ERROR_INIT NULL
#else
#define ERROR_INIT /**/
#endif

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "_connect",
  NULL,
  -1,
  connect_methods,
  NULL,
  NULL,
  NULL,
  NULL
};
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit__connect(void)
#else
init_connect(void)
#endif
{
    PyObject* m;

    PyEval_InitThreads();

#if PY_MAJOR_VERSION >= 3
    m = PyModule_Create(&moduledef);
#else
    m = Py_InitModule("_connect", connect_methods);
#endif

    // Errors
    ConnectError = PyErr_NewException("chirp.ConnectError", NULL, NULL);
    Py_INCREF(ConnectError);
    PyModule_AddObject(m, "ConnectError", ConnectError);

    // Constants
    PyModule_AddIntMacro(m, CHIRP_CONNECT_STATE_NOT_CREATED);
    PyModule_AddIntMacro(m, CHIRP_CONNECT_STATE_STOPPED);
    PyModule_AddIntMacro(m, CHIRP_CONNECT_STATE_PAUSED);
    PyModule_AddIntMacro(m, CHIRP_CONNECT_STATE_RUNNING);
    PyModule_AddIntMacro(m, CHIRP_CONNECT_STATE_SENDING);
    PyModule_AddIntMacro(m, CHIRP_CONNECT_STATE_RECEIVING);
    PyModule_AddIntMacro(m, CHIRP_CONNECT_BUFFER_SIZE);


#if PY_MAJOR_VERSION >= 3
    return m;
#endif
}
