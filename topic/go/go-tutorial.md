# Go tutorial

[go mainpage](/topic/go/go.md)

## install
[Install](https://golang.org/doc/install)

## enviroment

```
faxi:~ faxi$ go
Go is a tool for managing Go source code.

Usage:

	go <command> [arguments]

The commands are:

	bug         start a bug report
	build       compile packages and dependencies
	clean       remove object files and cached files
	doc         show documentation for package or symbol
	env         print Go environment information
	fix         update packages to use new APIs
	fmt         gofmt (reformat) package sources
	generate    generate Go files by processing source
	get         download and install packages and dependencies
	install     compile and install packages and dependencies
	list        list packages or modules
	mod         module maintenance
	run         compile and run Go program
	test        test packages
	tool        run specified go tool
	version     print Go version
	vet         report likely mistakes in packages

Use "go help <command>" for more information about a command.

Additional help topics:

	buildmode   build modes
	c           calling between Go and C
	cache       build and test caching
	environment environment variables
	filetype    file types
	go.mod      the go.mod file
	gopath      GOPATH environment variable
	gopath-get  legacy GOPATH go get
	goproxy     module proxy protocol
	importpath  import path syntax
	modules     modules, module versions, and more
	module-get  module-aware go get
	packages    package lists and patterns
	testflag    testing flags
	testfunc    testing functions

Use "go help <topic>" for more information about that topic.
```

## GOPATH setting

[doc](https://github.com/golang/go/wiki/SettingGOPATH)

### $PATH
```
faxi:~ faxi$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/go/bin
faxi:hello faxi$ export PATH=$PATH:$(go env GOPATH)/bin
faxi:hello faxi$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/go/bin:/Users/faxi/go/bin
```

### $GOPATH
```
faxi:~ faxi$ echo $GOPATH

faxi:~ faxi$ export GOPATH=$HOME/go
faxi:~ faxi$ echo $GOPATH
/Users/faxi/go
```

### go env

GOROOT: installation files.
GOBIN: bin files.

```
faxi:~ faxi$ go env
GOARCH="amd64"
GOBIN=""
GOCACHE="/Users/faxi/Library/Caches/go-build"
GOEXE=""
GOFLAGS=""
GOHOSTARCH="amd64"
GOHOSTOS="darwin"
GOOS="darwin"
GOPATH="/Users/faxi/go"
GOPROXY=""
GORACE=""
GOROOT="/usr/local/go"
GOTMPDIR=""
GOTOOLDIR="/usr/local/go/pkg/tool/darwin_amd64"
GCCGO="gccgo"
CC="clang"
CXX="clang++"
CGO_ENABLED="1"
GOMOD=""
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
GOGCCFLAGS="-fPIC -m64 -pthread -fno-caret-diagnostics -Qunused-arguments -fmessage-length=0 -fdebug-prefix-map=/var/folders/r6/63t9wny559xc1_2dh8743g5w0000gp/T/go-build246818204=/tmp/go-build -gno-record-gcc-switches -fno-common"
```

### file directory

```
go_project     // go_project为GOPATH目录
  -- bin
     -- myApp1  // 编译生成
     -- myApp2  // 编译生成
     -- myApp3  // 编译生成
  -- pkg
  -- src
     -- myApp1     // project1
        -- models
        -- controllers
        -- others
        -- main.go 
     -- myApp2     // project2
        -- models
        -- controllers
        -- others
        -- main.go 
     -- myApp3     // project3
        -- models
        -- controllers
        -- others
        -- main.go
```

## hello world

```
$ mkdir $GOPATH/src/hello
```
hello.go
```
package main

import "fmt"

func main() {
	fmt.Println("Hello, world.")
}
```
install
```
$ go install /hello
```
run
```
faxi:bin faxi$ $GOPATH/bin/hello
hello, world
```
push
```
$ cd $GOPATH/src/github.com/user/hello
$ git init
Initialized empty Git repository in /home/user/work/src/github.com/user/hello/.git/
$ git add hello.go
$ git commit -m "initial commit"
[master (root-commit) 0b4507d] initial commit
 1 file changed, 1 insertion(+)
  create mode 100644 hello.go
```

## package

```
faxi:src faxi$ mkdir stringutil
faxi:src faxi$ cd stringutil/
```

reverse.go
```
// Package stringutil contains utility functions for working with strings.
package stringutil

// Reverse returns its argument string reversed rune-wise left to right.
func Reverse(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}
```

build
```
faxi:stringutil faxi$ vim reverse.go
faxi:stringutil faxi$ go build
```

import
```
package main

import (
	"fmt"

	"stringutil"
)

func main() {
	fmt.Println(stringutil.Reverse("!oG ,olleH"))
}
```

build
```
faxi:hello-reverse faxi$ vim hello-reverse.go
faxi:hello-reverse faxi$ go build
```

run
```
faxi:hello-reverse faxi$ ./hello-reverse
Hello, Go!!
```

## notes

根目录编译则bin文件在$GOPATH/bin下，否则bin文件在/src下。
```
faxi:bin faxi$ go install /Users/faxi/go/src/hello-reverse/
faxi:bin faxi$ ls
hello		hello-reverse
faxi:bin faxi$ hello-reverse
Hello, Go!!
```





