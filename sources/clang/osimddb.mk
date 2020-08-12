TARGETS_ALL += sources/clang/all
TARGETS_WIPE += sources/clang/wipe
TARGETS_UPDATE += sources/clang/update
TARGETS_PHONY += sources/clang/all sources/clang/update sources/clang/wipe

sources/clang/all: sources/clang/Headers

sources/clang/wipe:
	rm -rf sources/clang/Headers

sources/clang/update: sources/clang/Headers
	cd sources/clang/Headers && svn up

sources/clang/Headers:
	cd sources/clang && svn checkout https://github.com/llvm/llvm-project/trunk/clang/lib/Headers

TARGETS_PHONY += sources/clang/all
