#ifndef DDS_STUBS_H_
#define DDS_STUBS_H_

#include "ddsc/dds.h"
#include "bit.h"

dds_qos_t* create_dds_state_qos(int32_t depth);
dds_qos_t* create_dds_v_state_qos(int32_t depth);
dds_qos_t* create_dds_tl_state_qos(int32_t depth);

dds_qos_t* create_dds_event_qos();
const dds_topic_descriptor_t* skey_bvalue();
const dds_topic_descriptor_t* skey_svalue();

const dds_topic_descriptor_t* ikey_svalue();
const dds_topic_descriptor_t* ikey_bvalue();
const dds_topic_descriptor_t* ikey_svalue();
const dds_topic_descriptor_t* svalue();

dds_entity_t s_create_participant(int id);

dds_entity_t s_create_topic_sksv(dds_entity_t dp, const char* name);
dds_entity_t s_create_topic_sv(dds_entity_t dp, const char* name);

dds_entity_t s_create_pub(dds_entity_t dp);
dds_entity_t s_create_sub(dds_entity_t dp);

dds_entity_t s_create_pub_wp(dds_entity_t dp, const char* partition);
dds_entity_t s_create_sub_wp(dds_entity_t dp, const char* partition);

dds_entity_t s_create_state_reader(dds_entity_t s, dds_entity_t t);
dds_entity_t s_create_event_reader(dds_entity_t s, dds_entity_t t);

dds_entity_t s_create_state_reader_wf(dds_entity_t s, dds_entity_t t,  dds_on_data_available_fn f);
dds_entity_t s_create_event_reader_wf(dds_entity_t s, dds_entity_t t,  dds_on_data_available_fn  f);

dds_entity_t s_create_state_reader_wl(dds_entity_t s, dds_entity_t t,  dds_listener_t* l);
dds_entity_t s_create_event_reader_wl(dds_entity_t s, dds_entity_t t,  dds_listener_t* l);


dds_entity_t s_create_state_writer(dds_entity_t p, dds_entity_t t);
dds_entity_t s_create_event_writer(dds_entity_t p, dds_entity_t t);

int s_write_sksv(dds_entity_t w, const dds_bit_SKeySValue* v);
int s_write_sv(dds_entity_t w, const dds_bit_SValue* v);

int s_write_key_value(dds_entity_t w, const char* key, const char* value);
int s_write_value(dds_entity_t w, const char* value);

dds_bit_SKeySValue* s_take_sksv(dds_entity_t r);
int s_take_sksv_a(dds_entity_t r, dds_bit_SKeySValue* sample);
dds_bit_SValue* s_take_sv(dds_entity_t r);

#endif /* DDS_STUBS_H_ */
