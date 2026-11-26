# Appendice — riferimenti a `/usr` in cbuild

Generato da `tools/usr-inventory/usr_inventory.py --core-md` sul commit
`f4aac13d0426e3118e12bf4c4ff9f820eb8280aa` di `chimera-linux/cports`.
Non modificare a mano: rigenerare.

| Cat. | File:riga | Testo |
|---|---|---|
| A | `src/cbuild/build_style/gnu_configure.py:6` | `if (self.bldroot_path / "usr/bin/slibtool").exists():` |
| A | `src/cbuild/build_style/makefile.py:11` | `"PREFIX=/usr",` |
| A | `src/cbuild/build_style/makefile.py:40` | `self.make.install(["STRIP=true", "PREFIX=/usr"])` |
| A | `src/cbuild/build_style/perl_module.py:14` | `perlpathroot = "usr/lib/perl5/core_perl"` |
| A | `src/cbuild/build_style/perl_module.py:32` | `["-L" + str(self.profile.sysroot / "usr/lib"), "-lperl"], shell=True` |
| A | `src/cbuild/build_style/perl_module.py:35` | `incp = self.profile.sysroot / "usr/include"` |
| A | `src/cbuild/build_style/perl_module.py:68` | `["-L" + str(self.profile.sysroot / "usr/lib"), "-lperl"], shell=True` |
| A | `src/cbuild/build_style/python_pep517.py:13` | `"PYTHON_CROSS_LIBDIR": self.profile.sysroot / "usr/lib",` |
| A | `src/cbuild/build_style/python_pep517.py:15` | `/ f"usr/include/python{self.python_version}",` |
| A | `src/cbuild/build_style/ruby_gem.py:37` | `self.chroot_destdir / "usr/bin",` |
| A | `src/cbuild/build_style/u_boot.py:62` | `destp = "usr/lib/u-boot/" + self.pkgname.removeprefix("u-boot-")` |
| A | `src/cbuild/build_style/waf.py:12` | `"--prefix=/usr",` |
| A | `src/cbuild/build_style/waf.py:13` | `"--libdir=/usr/lib",` |
| A | `src/cbuild/core/build.py:384` | `pkg.take(f"usr/share/licenses/{pkg.pkgname}", missing_ok=True)` |
| A | `src/cbuild/core/chroot.py:108` | `tpath = f"usr/share/terminfo/{tinfo[0]}/{tinfo}"` |
| A | `src/cbuild/core/chroot.py:123` | `(paths.bldroot() / "usr/lib/sysusers.d/cbuild.conf").unlink(missing_ok=True)` |
| A | `src/cbuild/core/chroot.py:126` | `if (paths.bldroot() / "usr/bin/sd-sysusers").is_file():` |
| A | `src/cbuild/core/chroot.py:143` | `if not (paths.bldroot() / "usr" / "bin" / "sh").is_file():` |
| A | `src/cbuild/core/chroot.py:147` | `"../usr/share/zoneinfo/UTC"` |
| A | `src/cbuild/core/chroot.py:153` | `if (paths.bldroot() / "usr/bin/sd-tmpfiles").is_file():` |
| A | `src/cbuild/core/chroot.py:156` | `if (paths.bldroot() / "usr/bin/update-ca-certificates").is_file():` |
| A | `src/cbuild/core/chroot.py:295` | `(path / "usr/lib/apk/db").mkdir(parents=True, exist_ok=True)` |
| A | `src/cbuild/core/chroot.py:302` | `(path / "lib").symlink_to("usr/lib")` |
| A | `src/cbuild/core/chroot.py:304` | `(path / "usr/lib/apk/db/installed").touch()` |
| A | `src/cbuild/core/chroot.py:680` | `defpath += ["/usr/bin"]` |
| A | `src/cbuild/core/paths.py:61` | `sapk = bldroot() / "usr/bin/apk.static"` |
| A | `src/cbuild/core/profile.py:172` | `f"/usr/lib/llvm{lver}/lib/clang/{lver}/lib/{prof._triplet}/libclang_rt.ubsan_standalone.a"` |
| A | `src/cbuild/core/profile.py:211` | `bflags = ["-isystem", paths.bldroot() / "usr/include"]` |
| A | `src/cbuild/core/profile.py:217` | `bflags += ["-isystem", f"/usr/lib/llvm{tmpl.llvm_version}/include"]` |
| A | `src/cbuild/core/profile.py:233` | `"-L" + str(paths.bldroot() / "usr/lib"),` |
| A | `src/cbuild/core/profile.py:234` | `"-Wl,-rpath-link=" + str(paths.bldroot() / "usr/lib"),` |
| A | `src/cbuild/core/profile.py:241` | `bflags.append(f"-L/usr/lib/llvm{tmpl.llvm_version}/lib")` |
| A | `src/cbuild/core/profile.py:254` | `self.sysroot / "usr",` |
| A | `src/cbuild/core/profile.py:409` | `return pathlib.Path("/usr") / self.triplet` |
| A | `src/cbuild/core/scanelf.py:278` | `libcp = paths.bldroot() / rsroot / "usr/lib/libc.so"` |
| A | `src/cbuild/core/scanelf.py:308` | `if fparts[0] != "usr" or fparts[1] == "include" or fparts[1] == "share":` |
| B | `src/cbuild/core/template.py:1952` | `binpath += ["/usr/lib/ccache/bin"]` |
| B | `src/cbuild/core/template.py:1956` | `and (self.bldroot_path / "usr/bin/sccache").exists()` |
| B | `src/cbuild/core/template.py:1958` | `cenv["RUSTC_WRAPPER"] = "/usr/bin/sccache"` |
| B | `src/cbuild/core/template.py:2175` | `f"usr/share/bash-completion/completions/{sfx}",` |
| B | `src/cbuild/core/template.py:2180` | `f"usr/share/zsh/site-functions/_{sfx}", glob, True` |
| B | `src/cbuild/core/template.py:2183` | `f"usr/share/fish/vendor_completions.d/{sfx}.fish",` |
| B | `src/cbuild/core/template.py:2187` | `return self.uninstall(f"usr/bin/{sfx}", glob, missing_ok)` |
| B | `src/cbuild/core/template.py:2189` | `return self.uninstall(f"usr/lib/{sfx}", glob, missing_ok)` |
| B | `src/cbuild/core/template.py:2192` | `f"usr/share/man/**/man{sfx[sfx.rfind('.') + 1 :]}/{sfx}",` |
| B | `src/cbuild/core/template.py:2314` | `self.install_file(src, "usr/bin", mode, name, glob)` |
| B | `src/cbuild/core/template.py:2317` | `self.install_file(src, "usr/lib", mode, name, glob)` |
| B | `src/cbuild/core/template.py:2320` | `self.install_dir("usr/share/man")` |
| B | `src/cbuild/core/template.py:2321` | `manbase = self.destdir / "usr/share/man"` |
| B | `src/cbuild/core/template.py:2364` | `src, "usr/share/licenses/" + (pkgname or self.pkgname), 0o644, name` |
| B | `src/cbuild/core/template.py:2373` | `src, "usr/share/bash-completion/completions", name=name` |
| B | `src/cbuild/core/template.py:2377` | `src, "usr/share/zsh/site-functions", name=f"_{name}"` |
| B | `src/cbuild/core/template.py:2382` | `"usr/share/fish/vendor_completions.d",` |
| B | `src/cbuild/core/template.py:2387` | `src, "usr/share/nushell/vendor/autoload", name=f"{name}.nu"` |
| B | `src/cbuild/core/template.py:2396` | `self.install_file(src, "usr/lib/dinit.d/user", name=svname)` |
| B | `src/cbuild/core/template.py:2398` | `self.install_dir("usr/lib/dinit.d/user/boot.d")` |
| B | `src/cbuild/core/template.py:2400` | `f"usr/lib/dinit.d/user/boot.d/{svname}", f"../{svname}"` |
| B | `src/cbuild/core/template.py:2404` | `self.install_file(src, "usr/lib/dinit.d", name=svname)` |
| B | `src/cbuild/core/template.py:2406` | `self.install_dir("usr/lib/dinit.d/boot.d")` |
| B | `src/cbuild/core/template.py:2408` | `f"usr/lib/dinit.d/boot.d/{svname}", f"../{svname}"` |
| B | `src/cbuild/core/template.py:2413` | `self.install_file(src, "usr/lib/tmpfiles.d", name=f"{svname}.conf")` |
| B | `src/cbuild/core/template.py:2417` | `self.install_file(src, "usr/lib/sysusers.d", name=f"{svname}.conf")` |
| B | `src/cbuild/core/template.py:2422` | `dstp = "usr/share/initramfs-tools/hooks"` |
| B | `src/cbuild/core/template.py:2424` | `dstp = f"usr/share/initramfs-tools/scripts/{stype}"` |
| B | `src/cbuild/core/template.py:2441` | `self.install_dir("usr/lib/shells.d")` |
| B | `src/cbuild/core/template.py:2444` | `f"usr/lib/shells.d/{os.path.basename(s)}", s, absolute=True` |
| B | `src/cbuild/core/template.py:2458` | `for f in (pkg.parent.destdir / "usr/lib").rglob("*.a"):` |
| B | `src/cbuild/core/template.py:2485` | `pkg.take("usr/lib/dinit.d/boot.d", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2486` | `pkg.take("usr/lib/dinit.d/user/boot.d", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2492` | `pkg.take("usr/share/bash-completion", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2497` | `pkg.take("usr/share/fish/completions", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2498` | `pkg.take("usr/share/fish/vendor_completions.d", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2502` | `pkg.take("usr/share/locale", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2504` | `pkg.take("usr/share/*/i18n/**/*.qm", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2505` | `pkg.take("usr/share/*/translations/**/*.qm", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2518` | `lambda p: p.take("usr/share/man", missing_ok=True),` |
| B | `src/cbuild/core/template.py:2526` | `lambda p: p.take("usr/lib/dinit.d", missing_ok=True),` |
| B | `src/cbuild/core/template.py:2532` | `lambda p: p.take("usr/share/initramfs-tools", missing_ok=True),` |
| B | `src/cbuild/core/template.py:2538` | `lambda p: p.take("usr/lib/udev", missing_ok=True),` |
| B | `src/cbuild/core/template.py:2550` | `lambda p: p.take("usr/share/zsh/site-functions", missing_ok=True),` |
| B | `src/cbuild/core/template.py:2562` | `lambda p: p.take("usr/share/nushell/vendor/autoload", missing_ok=True),` |
| B | `src/cbuild/core/template.py:2728` | `f"usr/share/man/**/man1/{p.name}.1", True` |
| B | `src/cbuild/core/template.py:2731` | `f"usr/share/man/**/man8/{p.name}.8", True` |
| B | `src/cbuild/core/template.py:2734` | `f"usr/share/bash-completion/completions/{p.name}",` |
| B | `src/cbuild/core/template.py:2738` | `f"usr/share/zsh/site-functions/_{p.name}",` |
| B | `src/cbuild/core/template.py:2742` | `f"usr/share/fish/vendor_completions.d/{p.name}.fish",` |
| B | `src/cbuild/core/template.py:2748` | `f"usr/bin/{sfx}", missing_ok, _take_mancmd` |
| B | `src/cbuild/core/template.py:2751` | `return self._take_impl(f"usr/lib/{sfx}", missing_ok)` |
| B | `src/cbuild/core/template.py:2755` | `f"usr/share/man/**/man{sfx[dot + 1 :]}/{sfx}",` |
| B | `src/cbuild/core/template.py:2767` | `self.take("usr/lib/*.a")` |
| B | `src/cbuild/core/template.py:2770` | `for f in (self.parent.destdir / "usr/bin").glob("*-config"):` |
| B | `src/cbuild/core/template.py:2772` | `self.take(f"usr/bin/{f.name}")` |
| B | `src/cbuild/core/template.py:2773` | `self.take("usr/lib/*.a", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2779` | `for f in (self.parent.destdir / "usr/lib").glob("*.so"):` |
| B | `src/cbuild/core/template.py:2781` | `self.take(f"usr/lib/{f.name}")` |
| B | `src/cbuild/core/template.py:2794` | `self.take(f"usr/lib/{f.name}")` |
| B | `src/cbuild/core/template.py:2795` | `self.take("usr/lib/pkgconfig", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2796` | `self.take("usr/lib/cmake", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2797` | `self.take("usr/lib/glade/modules", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2798` | `self.take("usr/lib/qt6/plugins/designer", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2799` | `self.take("usr/include", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2800` | `self.take("usr/share/cmake", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2801` | `self.take("usr/share/pkgconfig", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2802` | `self.take("usr/share/aclocal", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2803` | `self.take("usr/share/gettext", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2804` | `self.take("usr/share/vala/vapi", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2805` | `self.take("usr/share/gir-[0-9]*", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2806` | `self.take("usr/share/glade/catalogs", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2808` | `mpath = self.parent.destdir / "usr/share/man/man1"` |
| B | `src/cbuild/core/template.py:2811` | `self.take(f"usr/share/man/**/man1/{f.name}")` |
| B | `src/cbuild/core/template.py:2812` | `self.take(f"usr/share/man/**/man[{man}]", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2815` | `self.take("usr/share/doc", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2816` | `self.take("usr/share/info", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2817` | `self.take("usr/share/html", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2818` | `self.take("usr/share/licenses", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2819` | `self.take("usr/share/gtk-doc", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2820` | `self.take("usr/share/ri", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2821` | `self.take("usr/share/help", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2822` | `self.take("usr/share/devhelp/books", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2825` | `self.take("usr/lib/lib*.so.[0-9]*")` |
| B | `src/cbuild/core/template.py:2826` | `self.take("usr/lib/girepository-[0-9]*", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2829` | `self.take("usr/bin/*")` |
| B | `src/cbuild/core/template.py:2830` | `self.take("usr/share/bash-completion", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2831` | `self.take("usr/share/zsh", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2832` | `self.take("usr/share/fish/completions", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2833` | `self.take("usr/share/fish/vendor_completions.d", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2834` | `self.take("usr/share/nushell/vendor/autoload", missing_ok=True)` |
| B | `src/cbuild/core/template.py:2836` | `self.take(f"usr/share/man/**/man[{man}]", missing_ok=True)` |
| A | `src/cbuild/hooks/destdir/002_uncompress_manpages.py:6` | `for f in (pkg.destdir / "usr/share/man").rglob("*.*"):` |
| A | `src/cbuild/hooks/destdir/003_remove_misc.py:2` | `(pkg.destdir / "usr/lib/charset.alias").unlink(missing_ok=True)` |
| A | `src/cbuild/hooks/destdir/003_remove_misc.py:3` | `(pkg.destdir / "usr/share/info/dir").unlink(missing_ok=True)` |
| A | `src/cbuild/hooks/destdir/007_strip_debug.py:26` | `dbgdir = pkg.destdir / "usr/lib/debug"` |
| A | `src/cbuild/hooks/destdir/007_strip_debug.py:145` | `if not (pkg.destdir / "usr/lib/debug").is_dir():` |
| A | `src/cbuild/hooks/destdir/007_strip_debug.py:149` | `(ddest / "usr/lib").mkdir(parents=True, exist_ok=True)` |
| A | `src/cbuild/hooks/destdir/007_strip_debug.py:153` | `shutil.move(pkg.destdir / "usr/lib/debug", ddest / "usr/lib")` |
| A | `src/cbuild/hooks/destdir/007_strip_debug.py:158` | `for f in (pkg.destdir / "usr/lib").iterdir():` |
| A | `src/cbuild/hooks/destdir/007_strip_debug.py:161` | `(pkg.destdir / "usr/lib").rmdir()` |
| A | `src/cbuild/hooks/destdir/008_rename_python_bindings.py:11` | `for v in (pkg.destdir / "usr/lib").glob(` |
| A | `src/cbuild/hooks/destdir/009_remove_pkgconf_sysroot.py:6` | `sr = str(pkg.rparent.profile.sysroot / "usr")` |
| A | `src/cbuild/hooks/destdir/009_remove_pkgconf_sysroot.py:8` | `for f in pkg.destdir.glob("usr/*/pkgconfig/*.pc"):` |
| A | `src/cbuild/hooks/destdir/009_remove_pkgconf_sysroot.py:16` | `outf.write(ln.replace(sr, "/usr"))` |
| A | `src/cbuild/hooks/destdir/100_rewrite_python_shebang.py:7` | `default_shebang = b"#!/usr/bin/python3"` |
| A | `src/cbuild/hooks/destdir/100_rewrite_python_shebang.py:35` | `shebang = b"#!/usr/bin/python" + majver` |
| A | `src/cbuild/hooks/destdir/199_recompress_manpages.py:15` | `manbase = pkg.destdir / "usr/share/man"` |
| A | `src/cbuild/hooks/destdir/199_recompress_manpages.py:38` | `/ "usr/share/man"` |
| A | `src/cbuild/hooks/destdir/999_kernel_keys.py:7` | `db = pkg.destdir / "usr/src"` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:75` | `fdvn = f"/usr/lib/{dvn}"` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:197` | `if (pkg.destdir / "usr/lib/pkgconfig/libpkgconf.pc").exists():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:206` | `if (hsr / "usr/lib/pkgconfig").is_dir():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:207` | `pcpaths.append(str(sr / "usr/lib/pkgconfig"))` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:208` | `if (hsr / "usr/share/pkgconfig").is_dir():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:209` | `pcpaths.append(str(sr / "usr/share/pkgconfig"))` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:212` | `if (sp.destdir / "usr/lib/pkgconfig").is_dir():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:213` | `pcpaths.append(str(sp.chroot_destdir / "usr/lib/pkgconfig"))` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:214` | `if (sp.destdir / "usr/share/pkgconfig").is_dir():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:215` | `pcpaths.append(str(sp.chroot_destdir / "usr/share/pkgconfig"))` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:217` | `if (pkg.rparent.destdir / "usr/lib/pkgconfig").is_dir():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:218` | `pcpaths.append(str(pkg.rparent.chroot_destdir / "usr/lib/pkgconfig"))` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:219` | `if (pkg.rparent.destdir / "usr/share/pkgconfig").is_dir():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:220` | `pcpaths.append(str(pkg.rparent.chroot_destdir / "usr/share/pkgconfig"))` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:230` | `pkg.rparent.profile.sysroot / "usr/lib/pkgconfig"` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:273` | `if (pkg.destdir / f"usr/lib/pkgconfig/{pname}.pc").exists():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:275` | `elif (pkg.destdir / f"usr/share/pkgconfig/{pname}.pc").exists():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:280` | `for f in pkg.destdir.glob("usr/lib/pkgconfig/*.pc"):` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:283` | `for f in pkg.destdir.glob("usr/share/pkgconfig/*.pc"):` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:290` | `if (sp.destdir / f"usr/lib/pkgconfig/{pn}.pc").exists():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:292` | `if (sp.destdir / f"usr/share/pkgconfig/{pn}.pc").exists():` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:353` | `pth = pkg.destdir / "usr/lib/dinit.d"` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:366` | `for f in pkg.destdir.glob("usr/lib/dinit.d/*"):` |
| A | `src/cbuild/hooks/pkg/001_runtime_deps.py:369` | `for f in pkg.destdir.glob("usr/lib/dinit.d/user/*"):` |
| A | `src/cbuild/hooks/pkg/002_provides.py:39` | `for f in pkg.destdir.glob("usr/bin/*"):` |
| A | `src/cbuild/hooks/pkg/002_provides.py:48` | `f"  \f[cyan]cmd: \f[orange]{f.name}\f[] from \f[green]usr/bin\f[]"` |
| A | `src/cbuild/hooks/pkg/002_provides.py:145` | `for f in pkg.destdir.glob("usr/lib/pkgconfig/*.pc"):` |
| A | `src/cbuild/hooks/pkg/002_provides.py:148` | `for f in pkg.destdir.glob("usr/share/pkgconfig/*.pc"):` |
| A | `src/cbuild/hooks/pkg/002_provides.py:166` | `return str(root) == "usr/lib"` |
| A | `src/cbuild/hooks/pkg/002_provides.py:284` | `for f in pkg.destdir.glob("usr/lib/dinit.d/*"):` |
| A | `src/cbuild/hooks/pkg/002_provides.py:292` | `for f in pkg.destdir.glob("usr/lib/dinit.d/user/*"):` |
| A | `src/cbuild/hooks/pkg/005_py_dep.py:16` | `for pver in (pkg.destdir / "usr/lib").glob("python3.*"):` |
| A | `src/cbuild/hooks/pkg/007_trigger_deps.py:12` | `"usr/share/ca-certificates": "ca-certificates",` |
| A | `src/cbuild/hooks/pkg/097_dinit_style.py:66` | `pd = pkg.destdir / "usr/lib/dinit.d"` |
| A | `src/cbuild/hooks/pkg/098_lint.py:13` | `for v in (pkg.destdir / "usr/lib").rglob("*.a"):` |
| A | `src/cbuild/hooks/pkg/098_lint.py:32` | `lpath = pkg.destdir / "usr/share/licenses"` |
| A | `src/cbuild/hooks/pkg/098_lint.py:35` | `lpath = pkg.destdir.parent / f"{pkg.pkgname}-doc/usr/share/licenses"` |
| A | `src/cbuild/hooks/pkg/098_lint.py:51` | `"/etc/bash_completion.d found, should be /usr/share/bash-completion"` |
| A | `src/cbuild/hooks/pkg/098_lint.py:54` | `for p in (pkg.destdir / "usr/share/bash-completion/completions").iterdir():` |
| A | `src/cbuild/hooks/pkg/098_lint.py:55` | `if not (pkg.parent.destdir / "usr/bin" / p.name).exists():` |
| A | `src/cbuild/hooks/pkg/098_lint.py:60` | `for p in (pkg.destdir / "usr/share/zsh/site-functions").iterdir():` |
| A | `src/cbuild/hooks/pkg/098_lint.py:64` | `pkg.parent.destdir / "usr/bin" / p.name.removeprefix("_")` |
| A | `src/cbuild/hooks/pkg/098_lint.py:70` | `if (pkg.destdir / "usr/share/fish/completions").exists():` |
| A | `src/cbuild/hooks/pkg/098_lint.py:72` | `"fish completions need to go in usr/share/fish/vendor_completions.d, not usr/share/fish/completions"` |
| A | `src/cbuild/hooks/pkg/098_lint.py:75` | `for p in (pkg.destdir / "usr/share/fish/vendor_completions.d").iterdir():` |
| A | `src/cbuild/hooks/pkg/098_lint.py:77` | `pkg.parent.destdir / "usr/bin" / p.name.removesuffix(".fish")` |
| A | `src/cbuild/hooks/pkg/098_lint.py:119` | `"usr/include": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:120` | `"usr/lib/cmake": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:121` | `"usr/lib/glade/modules": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:122` | `"usr/lib/pkgconfig": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:123` | `"usr/share/pkgconfig": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:124` | `"usr/share/vala/vapi": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:125` | `"usr/share/gir-1.0": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:126` | `"usr/share/aclocal": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:127` | `"usr/share/gettext": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:128` | `"usr/share/cmake": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:129` | `"usr/share/glade/catalogs": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:139` | `for v in pkg.destdir.rglob("usr/lib/*.so"):` |
| A | `src/cbuild/hooks/pkg/098_lint.py:145` | `for v in pkg.destdir.rglob("usr/bin/*-config"):` |
| A | `src/cbuild/hooks/pkg/098_lint.py:165` | `"usr": True,` |
| A | `src/cbuild/hooks/pkg/098_lint.py:212` | `"usr",` |
| A | `src/cbuild/hooks/pkg/098_lint.py:214` | `if (pkg.destdir / "usr" / d).exists():` |
| A | `src/cbuild/hooks/pkg/098_lint.py:215` | `pkg.log_red(f"forbidden path '/usr/{d}'")` |
| A | `src/cbuild/hooks/pkg/098_lint.py:220` | `and (pkg.destdir / "usr/share/pixmaps").exists()` |
| A | `src/cbuild/hooks/pkg/098_lint.py:223` | `"'/usr/share/pixmaps' exists, '/usr/share/icons' is preferred for application icons"` |
| A | `src/cbuild/hooks/pkg/098_lint.py:268` | `pkg.log_red(f"{d} should go in /usr{exp_dest}, not /etc")` |
| A | `src/cbuild/hooks/pkg/098_lint.py:283` | `pkg.log_red(f"{d} should go in /usr/share, not /etc")` |
| A | `src/cbuild/hooks/pkg/098_lint.py:288` | `if (pkg.destdir / "usr" / d).exists():` |
| A | `src/cbuild/hooks/pkg/098_lint.py:289` | `pkg.log_red(f"{d} should go in /usr/share, not /usr")` |
| A | `src/cbuild/hooks/pkg/098_lint.py:293` | `for d in (pkg.destdir / "usr/lib").glob("python*"):` |
| A | `src/cbuild/hooks/pkg/098_lint.py:307` | `"usr",` |
| A | `src/cbuild/hooks/pkg/098_lint.py:315` | `for d in (pkg.destdir / "usr/src").glob("linux-headers-*/certs"):` |
| A | `src/cbuild/hooks/prepare/000_script_wrapper.py:25` | `"/usr/bin/cbuild-cross-cc"` |
| A | `src/cbuild/hooks/prepare/000_script_wrapper.py:38` | `export PKG_CONFIG_PATH="{sroot}/usr/lib/pkgconfig:{sroot}/usr/share/pkgconfig${{PKG_CONFIG_PATH:+:${{PKG_CONFIG_PATH}}}}"` |
| A | `src/cbuild/hooks/prepare/000_script_wrapper.py:39` | `export PKG_CONFIG_LIBDIR="{sroot}/usr/lib/pkgconfig${{PKG_CONFIG_LIBDIR:+:${{PKG_CONFIG_LIBDIR}}}}"` |
| A | `src/cbuild/hooks/prepare/000_script_wrapper.py:40` | `exec /usr/bin/pkg-config "$@"` |
| A | `src/cbuild/hooks/prepare/001_prepare_users.py:17` | `if not (paths.bldroot() / "usr/bin/sd-sysusers").exists():` |
| A | `src/cbuild/hooks/prepare/001_prepare_users.py:20` | `bp = paths.bldroot() / "usr/lib/sysusers.d"` |
| A | `src/cbuild/hooks/setup/000_env_pkg_config.py:8` | `usrdir = paths.bldroot() / "usr"` |
| A | `src/cbuild/hooks/setup/001_lang_vers.py:8` | `pypath = paths.bldroot() / "usr/bin/python"` |
| A | `src/cbuild/hooks/setup/001_lang_vers.py:11` | `pkg.error("/usr/bin/python must be a symbolic link")` |
| A | `src/cbuild/hooks/setup/001_lang_vers.py:28` | `rbpath = paths.bldroot() / "usr/lib/ruby"` |
| A | `src/cbuild/hooks/setup/002_llvm.py:9` | `usr = paths.bldroot() / "usr"` |
| A | `src/cbuild/util/cargo.py:39` | `"GETTEXT_BIN_DIR": "/usr/bin",` |
| A | `src/cbuild/util/cargo.py:40` | `"GETTEXT_LIB_DIR": str(sroot / "usr/lib/gettext"),` |
| A | `src/cbuild/util/cargo.py:247` | `"/usr",` |
| A | `src/cbuild/util/cargo.py:275` | `str(tmpl.chroot_destdir / "usr"),` |
| A | `src/cbuild/util/cargo.py:306` | `"/usr",` |
| A | `src/cbuild/util/cmake.py:31` | `SET(CMAKE_FIND_ROOT_PATH  "{paths.bldroot() / "usr"};{paths.bldroot()}")` |
| A | `src/cbuild/util/cmake.py:72` | `SET(CMAKE_FIND_ROOT_PATH  "{sroot / "usr"};{sroot}")` |
| A | `src/cbuild/util/cmake.py:83` | `f"-DCMAKE_AR=/usr/bin/{pkg.get_tool('AR')}",` |
| A | `src/cbuild/util/cmake.py:84` | `f"-DCMAKE_NM=/usr/bin/{pkg.get_tool('NM')}",` |
| A | `src/cbuild/util/cmake.py:85` | `f"-DCMAKE_RANLIB=/usr/bin/{pkg.get_tool('RANLIB')}",` |
| A | `src/cbuild/util/cmake.py:90` | `proot = pkg.profile.sysroot / f"usr/lib/llvm{pkg.llvm_version}"` |
| A | `src/cbuild/util/cmake.py:103` | `"-DCMAKE_INSTALL_PREFIX=/usr",` |
| A | `src/cbuild/util/gnu_configure.py:8` | `"lt_cv_sys_lib_dlsearch_path_spec": "/usr/lib64 /usr/lib32 /usr/lib /lib /usr/local/lib"` |
| A | `src/cbuild/util/gnu_configure.py:84` | `"--prefix=/usr",` |
| A | `src/cbuild/util/gnu_configure.py:86` | `"--sbindir=/usr/bin",` |
| A | `src/cbuild/util/gnu_configure.py:87` | `"--bindir=/usr/bin",` |
| A | `src/cbuild/util/gnu_configure.py:88` | `"--libdir=/usr/lib",` |
| A | `src/cbuild/util/gnu_configure.py:89` | `"--libexecdir=/usr/lib",` |
| A | `src/cbuild/util/gnu_configure.py:90` | `"--mandir=/usr/share/man",` |
| A | `src/cbuild/util/gnu_configure.py:91` | `"--infodir=/usr/share/info",` |
| A | `src/cbuild/util/gnu_configure.py:99` | `if (pkg.bldroot_path / "usr/bin/slibtoolize").exists():` |
| A | `src/cbuild/util/gnu_configure.py:103` | `eenv["ACLOCAL"] = "aclocal --aclocal-path=/usr/share/slibtool"` |
| A | `src/cbuild/util/linux.py:99` | `(pkg.destdir / "usr/lib/modules").glob(` |
| A | `src/cbuild/util/linux.py:137` | `for f in (paths.bldroot() / "usr/lib/modules").iterdir():` |
| A | `src/cbuild/util/linux.py:151` | `return paths.bldroot() / f"usr/src/{modname}-{modver}"` |
| A | `src/cbuild/util/linux.py:168` | `_call_ckms(pkg, kver, "add", f"/usr/src/{modname}-{modver}")` |
| A | `src/cbuild/util/linux.py:192` | `modbase = "usr/lib/modules"` |
| A | `src/cbuild/util/meson.py:36` | `llvm-config = '/usr/bin/llvm-config'` |
| A | `src/cbuild/util/meson.py:37` | `rust = ['rustc', '--target', '{pkg.profile.triplet}', '--sysroot', '{pkg.profile.sysroot / "usr"}']` |
| A | `src/cbuild/util/meson.py:84` | `"--prefix=/usr",` |
| A | `src/cbuild/util/meson.py:85` | `"--libdir=/usr/lib",` |
| A | `src/cbuild/util/meson.py:86` | `"--libexecdir=/usr/lib",` |
| A | `src/cbuild/util/meson.py:87` | `"--bindir=/usr/bin",` |
| A | `src/cbuild/util/meson.py:88` | `"--sbindir=/usr/bin",` |
| A | `src/cbuild/util/meson.py:89` | `"--includedir=/usr/include",` |
| A | `src/cbuild/util/meson.py:90` | `"--datadir=/usr/share",` |
| A | `src/cbuild/util/meson.py:91` | `"--mandir=/usr/share/man",` |
| A | `src/cbuild/util/meson.py:92` | `"--infodir=/usr/share/info",` |
| A | `src/cbuild/util/strip.py:25` | `"/usr/bin/" + pkg.rparent.get_tool("STRIP"),` |
