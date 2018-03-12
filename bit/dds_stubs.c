#include "dds_stubs.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define MAX_SAMPLES 1

dds_qos_t*
create_dds_state_qos(int32_t depth) {
  dds_qos_t* state_qos = dds_qos_create();
  dds_qset_reliability(state_qos, DDS_RELIABILITY_RELIABLE, DDS_INFINITY);
  dds_qset_durability(state_qos, DDS_DURABILITY_VOLATILE);
  dds_qset_history(state_qos, DDS_HISTORY_KEEP_LAST, depth);
  dds_qset_writer_data_lifecycle(state_qos, false);
  return state_qos;
}

dds_qos_t*
create_dds_event_qos() {
  dds_qos_t* event_qos = dds_qos_create();
  dds_qset_reliability(event_qos, DDS_RELIABILITY_RELIABLE, DDS_INFINITY);
  dds_qset_history(event_qos, DDS_HISTORY_KEEP_ALL, DDS_LENGTH_UNLIMITED);
  return event_qos;
}

dds_qos_t*
dds_state_qos(int32_t depth) {
  dds_qos_t* state_qos = create_dds_state_qos(depth);
  return state_qos;
}

dds_qos_t*
dds_event_qos() {
  dds_qos_t* event_qos = create_dds_event_qos();
  return event_qos;
}

const dds_topic_descriptor_t*
skey_bvalue() {
  return &dds_bit_SKeyBValue_desc;
}

const dds_topic_descriptor_t*
skey_svalue() {
  return &dds_bit_SValue_desc;
}

const dds_topic_descriptor_t*
ikey_svalue() {
  return &dds_bit_IKeySValue_desc;
}

const dds_topic_descriptor_t*
ikey_bvalue() {
  return &dds_bit_IKeyBValue_desc;
}

const dds_topic_descriptor_t*
svalue() {
  return &dds_bit_SValue_desc;
}

dds_entity_t
s_create_participant(int id) {
  return dds_create_participant(id, NULL, NULL);
}

dds_entity_t
s_create_topic_sksv(dds_entity_t dp, const char* name) {
  return dds_create_topic(dp, &dds_bit_SKeySValue_desc, name, NULL, NULL);
}

dds_entity_t
s_create_topic_sv(dds_entity_t dp, const char* name) {
  return dds_create_topic(dp, &dds_bit_SValue_desc, name, NULL, NULL);
}

dds_entity_t
s_create_pub_wp(dds_entity_t dp, const char* partition) {
  dds_qos_t* qos = dds_qos_create();
  const char * ps[1] = { partition };
  dds_qset_partition(qos, 1, &ps[0]);
  return dds_create_publisher(dp, qos, NULL);
}

dds_entity_t
s_create_sub_wp(dds_entity_t dp, const char* partition) {
  dds_qos_t* qos = dds_qos_create();
  const char * ps[1] = { partition };
  dds_qset_partition(qos, 1, &ps[0]);
  return dds_create_subscriber(dp, qos, NULL);
}

dds_entity_t
s_create_pub(dds_entity_t dp) {
  return dds_create_publisher(dp, NULL, NULL);
}

dds_entity_t
s_create_sub(dds_entity_t dp) {
  return dds_create_subscriber(dp, NULL, NULL);
}

dds_entity_t s_create_state_reader(dds_entity_t s, dds_entity_t t) {
  return dds_create_reader(s, t, dds_state_qos(1), NULL);
}

dds_entity_t
s_create_event_reader(dds_entity_t s, dds_entity_t t) {
  return dds_create_reader(s, t, dds_event_qos(), NULL);
}


void listener_wrapper(dds_entity_t rd, void* attch) {
  printf("stub:>>Listener Wrapper called!\n");
}

void callme_back(dds_on_data_available_fn f) {
  f(0, NULL);
}


dds_entity_t
s_create_state_reader_wl(dds_entity_t s, dds_entity_t t,  dds_listener_t* l) {
  return dds_create_reader(s, t, dds_state_qos(1), l);
}


dds_entity_t
s_create_event_reader_wl(dds_entity_t s, dds_entity_t t,  dds_listener_t* l) {
  return dds_create_reader(s, t, dds_event_qos(), l);
}


dds_entity_t
s_create_state_reader_wf(dds_entity_t s, dds_entity_t t,  dds_on_data_available_fn f) {
  dds_listener_t* l = dds_listener_create(NULL);
  dds_lset_data_available(l, f);
  return dds_create_reader(s, t, dds_state_qos(1), l);
}


dds_entity_t
s_create_event_reader_wf(dds_entity_t s, dds_entity_t t,  dds_on_data_available_fn  f) {
  dds_listener_t* l = dds_listener_create(NULL);
  dds_lset_data_available(l, f);
  return dds_create_reader(s, t, dds_event_qos(), l);
}


dds_entity_t s_create_state_writer(dds_entity_t p, dds_entity_t t) {
  return dds_create_writer(p, t, dds_state_qos(1), NULL);
}
dds_entity_t s_create_event_writer(dds_entity_t p, dds_entity_t t) {
  return dds_create_writer(p, t, dds_event_qos(), NULL);
}

int s_write_sksv(dds_entity_t w, const dds_bit_SKeySValue* v) {
  return dds_write(w, v);
}
int s_write_sv(dds_entity_t w, const dds_bit_SValue* v) {
  return dds_write(w, v);
}

int
s_write_key_value(dds_entity_t w, const char* key, const char* value) {
  dds_bit_SKeySValue sample = {(char*)key, (char*)value};
  return dds_write(w, &sample);
}

int
s_write_value(dds_entity_t w, const char* value) {
  const dds_bit_SValue sample = {(char*)value};
  return dds_write(w, &sample);
}

dds_bit_SKeySValue* s_take_sksv(dds_entity_t r) {
  void* samples[MAX_SAMPLES];
  samples[0] = dds_bit_SKeySValue__alloc ();
  dds_sample_info_t infos[MAX_SAMPLES];
  int n = dds_take(r, samples, infos, MAX_SAMPLES, MAX_SAMPLES);
  if (infos[0].valid_data) {
    return samples[0];
  }
  else {
    return NULL;
  }
}

int s_take_sksv_a(dds_entity_t r, dds_bit_SKeySValue* sample) {
  void* samples[MAX_SAMPLES];
  dds_bit_SKeySValue* s = dds_bit_SKeySValue__alloc ();
  samples[0] = s;
  dds_sample_info_t infos[MAX_SAMPLES];
  int n = dds_take(r, samples, infos, MAX_SAMPLES, MAX_SAMPLES);
  if (infos[0].valid_data) {
    sample->key = strdup(s->key);
    sample->value = strdup(s->value);
  }
  samples[0] = NULL;
  dds_bit_SKeySValue_free(s, DDS_FREE_ALL);
  return n;
}

dds_bit_SValue* s_take_sv(dds_entity_t r) {
  dds_bit_SValue* pv = malloc(sizeof(dds_bit_SValue));
  void* samples[1] = {pv};
  dds_sample_info_t infos[10];
  dds_take(r, samples, infos, 1, 1);
  if (infos[0].valid_data) {
    return pv;
  }
  else {
    free (pv);
    return NULL;
  }
}
