TARGETS_ALL =
TARGETS_CLEAN =
TARGETS_WIPE =
TARGETS_UPDATE =
TARGETS_PHONY = all clean ossimddb-all

all: ossimddb-all

include sources/osimddb.mk
include data/osimddb.mk

.PHONY: $(TARGETS_PHONY)

ossimddb-all: $(TARGETS_ALL)
clean: $(TARGETS_CLEAN)
update: $(TARGETS_UPDATE)
wipe: $(TARGETS_WIPE)
