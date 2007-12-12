#there's already a pop-before-smtp package in contribs, but this is another one written in c
%define name	pop-before-smtp-in-c
%define altname	pop-before-smtp
%define version	1.0
%define	rel	3
%define	release	%mkrel %{rel}

Summary:	Watch log for pop/imap auth, notify Postfix to allow relay
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{altname}-%{version}.tar.bz2
Source1:	%{altname}.init.bz2
Patch0:		%{altname}-maillog.patch.bz2
URL:		http://www.bluelavalamp.net/pop-before-smtp/
License:	GPL
Group:		System/Servers
Requires(post,preun):	rpm-helper
Requires:	postfix vm-pop3d
Conflicts:	%{altname}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Spam prevention requires preventing open relaying through email
servers. However, legit users want to be able to relay. If legit
users always stayed in one spot, they'd be easy to describe to the
daemon. However, what with roving laptops, logins from home, etc.,
legit users refuse to stay in one spot.

pop-before-smtp watches the mail log, looking for successful
pop/imap logins, and posts the originating IP address into a
database which can be checked by Postfix, to allow relaying for
people who have recently downloaded their email.

%prep
%setup -q -n %{altname}-%{version}
bzcat %{SOURCE1} > %{altname}.init
%patch0 -p0

%build
%{__cc} -DOPTIMIZE $RPM_OPT_FLAGS -o %{altname} %{altname}.c

%install
rm -rf $RPM_BUILD_ROOT
install -m755 %{altname} -D %{buildroot}%{_sbindir}/%{altname}
install -m755 %{altname}.init -D %{buildroot}%{_initrddir}/%{altname}

%post
%_post_service %{altname}

%preun
%_post_service %{altname}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES %{altname}.html
%{_sbindir}/%{altname}
%config(noreplace) %{_initrddir}/%{altname}

