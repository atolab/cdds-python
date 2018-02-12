#include "dds_stubs.h"
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

void run_pub() {
  dds_entity_t dp = s_create_participant(0);
  dds_entity_t p = s_create_pub(dp);
  // dds_entity_t p = s_create_pub_wp(dp, "alpha");
  dds_entity_t t = s_create_topic_sksv(dp, "KeyValue");
  dds_entity_t w = s_create_state_writer(p, t);

  char value[256];
  int i = 0;
  while (true) {
    printf("Writing...\n");
    sprintf(value, "value-%d", i);
    i++;
    s_write_key_value(w, "key", value);
    sleep(1);
  }
}

void listener(dds_entity_t rd, void* attch) {
  printf("Listener called!\n");
}

void run_sub() {
  dds_entity_t dp = s_create_participant(0);
  dds_entity_t s = s_create_sub(dp);
  // dds_entity_t s = s_create_sub_wp(dp, "alpha");
  dds_entity_t t = s_create_topic_sksv(dp, "KeyValue");
  dds_entity_t t2 = s_create_topic_sksv(dp, "KeyValue");
  
  dds_entity_t r = s_create_state_reader_wf(s, t, listener);

  while (true) {
      // dds_bit_SKeySValue* sample = s_take_sksv(r);
      // if (sample != NULL)
        // printf(">> (key: %s, value: - %s)\n", sample->key, sample->value);
      sleep(5);
  }
}

int main(int argc, char* argv[]) {
  if (argc == 1)
    run_pub();
  else
    run_sub();
  return 0;
}
