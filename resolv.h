/*
 * Copyright (c) 1983, 1987, 1989
 *    The Regents of the University of California.  All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the University nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

/*
 * Copyright (c) 2004 by Internet Systems Consortium, Inc. ("ISC")
 * Portions Copyright (c) 1996-1999 by Internet Software Consortium.
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL ISC BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
 * OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

/*%
 *	@(#)resolv.h	8.1 (Berkeley) 6/2/93
 * $FreeBSD: release/9.0.0/include/resolv.h 203964 2010-02-16 19:39:50Z imp $
 */

#ifndef _RESOLV_H_
#define	_RESOLV_H_

#include <sys/param.h>
#include <sys/types.h>
#include <sys/cdefs.h>
#include <stdio.h>
#include <netinet/in.h> /* struct in_addr */

/*%
 * Revision information.  This is the release date in YYYYMMDD format.
 * It can change every day so the right thing to do with it is use it
 * in preprocessor commands such as "#if (__RES > 19931104)".  Do not
 * compare for equality; rather, use it to determine whether your resolver
 * is new enough to contain a certain feature.
 */

#define	__RES	19960801

/*%
 * Resolver configuration file.
 * Normally not present, but may contain the address of the
 * initial name server(s) to query and the domain search list.
 */

#ifndef _PATH_RESCONF
#define	_PATH_RESCONF        "/etc/resolv.conf"
#endif

typedef enum { res_goahead, res_nextns, res_modified, res_done, res_error }
	res_sendhookact;

typedef res_sendhookact (*res_send_qhook)(struct sockaddr_in * const *ns,
					      const u_char **query,
					      int *querylen,
					      u_char *ans,
					      int anssiz,
					      int *resplen);

typedef res_sendhookact (*res_send_rhook)(const struct sockaddr_in *ns,
					      const u_char *query,
					      int querylen,
					      u_char *ans,
					      int anssiz,
					      int *resplen);

struct res_sym {
	int		number;	   /*%< Identifying number, like T_MX */
	const char *	name;	   /*%< Its symbolic name, like "MX" */
	const char *	humanname; /*%< Its fun name, like "mail exchanger" */
};

/*%
 * Global defines and variables for resolver stub.
 */
#define	MAXNS			3	/*%< max # name servers we'll track */
#define	MAXDFLSRCH		3	/*%< # default domain levels to try */
#define	MAXDNSRCH		6	/*%< max # domains in search path */
#define	LOCALDOMAINPARTS	2	/*%< min levels in name that is "local" */
#define	RES_TIMEOUT		5	/*%< min. seconds between retries */
#define	MAXRESOLVSORT		10	/*%< number of net to sort on */
#define	RES_MAXNDOTS		15	/*%< should reflect bit field size */

struct __res_state {
	int	retrans;	 	/*%< retransmission time interval */
	int	retry;			/*%< number of times to retransmit */
	u_long	options;		/*%< option flags - see below. */
	int	nscount;		/*%< number of name servers */
	struct sockaddr_in
		nsaddr_list[MAXNS];	/*%< address of name server */
#define	nsaddr	nsaddr_list[0]		/*%< for backward compatibility */
	u_short	id;			/*%< current message id */
	char	*dnsrch[MAXDNSRCH+1];	/*%< components of domain to search */
	char	defdname[256];		/*%< default domain (deprecated) */
	u_long	pfcode;			/*%< RES_PRF_ flags - see below. */
	unsigned ndots:4;		/*%< threshold for initial abs. query */
	unsigned nsort:4;		/*%< number of elements in sort_list[] */
	char	unused[3];
	struct {
		struct in_addr	addr;
		u_int32_t	mask;
	} sort_list[MAXRESOLVSORT];
	int	res_h_errno;		/*%< last one set for this context */
	char	pad[72];		/* on an i386 this means 512b total */
};

typedef struct __res_state *res_state;

/*%
 * Resolver options (keep these in synch with res_debug.c, please)
 */
#define RES_INIT	0x00000001	/*%< address initialized */
#define RES_DEBUG	0x00000002	/*%< print debug messages */
#define RES_AAONLY	0x00000004	/*%< authoritative answers only (!IMPL)*/
#define RES_USEVC	0x00000008	/*%< use virtual circuit */
#define RES_PRIMARY	0x00000010	/*%< query primary server only (!IMPL) */
#define RES_IGNTC	0x00000020	/*%< ignore truncation errors */
#define RES_RECURSE	0x00000040	/*%< recursion desired */
#define RES_DEFNAMES	0x00000080	/*%< use default domain name */
#define RES_STAYOPEN	0x00000100	/*%< Keep TCP socket open */
#define RES_DNSRCH	0x00000200	/*%< search up local domain tree */
#define	RES_INSECURE1	0x00000400	/*%< type 1 security disabled */
#define	RES_INSECURE2	0x00000800	/*%< type 2 security disabled */
#define	RES_NOALIASES	0x00001000	/*%< shuts off HOSTALIASES feature */
#define	RES_USE_INET6	0x00002000	/*%< use/map IPv6 in gethostbyname() */
#define	RES_NOTLDQUERY	0x00004000	/*%< Don't query TLD names */

#define RES_DEFAULT	(RES_RECURSE | RES_DEFNAMES | \
			 RES_DNSRCH)

/*%
 * Resolver "pfcode" values.  Used by dig.
 */
#define	RES_PRF_STATS	0x00000001
#define	RES_PRF_UPDATE	0x00000002
#define	RES_PRF_CLASS   0x00000004
#define	RES_PRF_CMD	0x00000008
#define	RES_PRF_QUES	0x00000010
#define	RES_PRF_ANS	0x00000020
#define	RES_PRF_AUTH	0x00000040
#define	RES_PRF_ADD	0x00000080
#define	RES_PRF_HEAD1	0x00000100
#define	RES_PRF_HEAD2	0x00000200
#define	RES_PRF_TTLID	0x00000400
#define	RES_PRF_HEADX	0x00000800
#define	RES_PRF_QUERY	0x00001000
#define	RES_PRF_REPLY	0x00002000
#define	RES_PRF_INIT	0x00004000
/*			0x00008000	*/

#define fp_nquery		__fp_nquery
#define fp_query		__fp_query
#define hostalias		__hostalias
#define p_query			__p_query
#define res_close		__res_close
#define res_init		__res_init
#define res_isourserver		__res_isourserver
#define res_mkquery		__res_mkquery
#define res_query		__res_query
#define res_querydomain		__res_querydomain
#define res_search		__res_search
#define res_send		__res_send

__BEGIN_DECLS
void		fp_nquery(const u_char *, int, FILE *);
void		fp_query(const u_char *, FILE *);
const char *	hostalias(const char *);
void		p_query(const u_char *);
void		res_close(void);
int		res_init(void);
int		res_isourserver(const struct sockaddr_in *);
int		res_mkquery(int, const char *, int, int, const u_char *,
				 int, const u_char *, u_char *, int);
int		res_query(const char *, int, int, u_char *, int);
int		res_querydomain(const char *, const char *, int, int,
				     u_char *, int);
int		res_search(const char *, int, int, u_char *, int);
int		res_send(const u_char *, int, u_char *, int);
__END_DECLS

extern struct __res_state _res;


extern const struct res_sym __p_class_syms[];
extern const struct res_sym __p_type_syms[];

/* Private routines shared between libc/net, named, nslookup and others. */
#define b64_ntop		__b64_ntop
#define b64_pton		__b64_pton
#define dn_comp			__dn_comp
#define dn_count_labels		__dn_count_labels
#define dn_expand		__dn_expand
#define dn_skipname		__dn_skipname
#define fp_resstat		__fp_resstat
#define loc_aton		__loc_aton
#define loc_ntoa		__loc_ntoa
#define p_cdname		__p_cdname
#define p_cdnname		__p_cdnname
#define fp_resstat		__fp_resstat
#define p_class			__p_class
#define p_fqname		__p_fqname
#define p_fqnname		__p_fqnname
#define p_option		__p_option
#define p_secstodate		__p_secstodate
#define p_section		__p_section
#define p_time			__p_time
#define p_type			__p_type
#define putlong			__putlong
#define putshort		__putshort
#define res_dnok		__res_dnok
#define res_hnok		__res_hnok
#define res_mailok		__res_mailok
#define res_nameinquery		__res_nameinquery
#define res_ownok		__res_ownok
#define res_queriesmatch	__res_queriesmatch
#define res_randomid		__res_randomid
#define sym_ntop		__sym_ntop
#define sym_ntos		__sym_ntos
#define sym_ston		__sym_ston
#define	res_send_setqhook	__res_send_setqhook
#define	res_send_setrhook	__res_send_setrhook
#define res_mkupdate		__res_mkupdate
#define res_mkupdrec		__res_mkupdrec
#define res_freeupdrec		__res_freeupdrec

__BEGIN_DECLS
int		res_hnok(const char *);
int		res_ownok(const char *);
int		res_mailok(const char *);
int		res_dnok(const char *);
int		sym_ston(const struct res_sym *, const char *, int *);
const char *	sym_ntos(const struct res_sym *, int, int *);
const char *	sym_ntop(const struct res_sym *, int, int *);
int		b64_ntop(u_char const *, size_t, char *, size_t);
int		b64_pton(char const *, u_char *, size_t);
int		loc_aton(const char *, u_char *);
const char *	loc_ntoa(const u_char *, char *);
int		dn_skipname(const u_char *, const u_char *);
void		fp_resstat(struct __res_state *, FILE *);
void		putlong(u_int32_t, u_char *);
void		putshort(u_int16_t, u_char *);
const char *	p_class(int);
const char *	p_time(u_int32_t);
const char *	p_type(int);
const u_char *	p_cdnname(const u_char *, const u_char *, int, FILE *);
const u_char *	p_cdname(const u_char *, const u_char *, FILE *);
const u_char *	p_fqnname(const u_char *, const u_char *, int, char *, int);
const u_char *	p_fqname(const u_char *, const u_char *, FILE *);
const char *	p_option(u_long);
char *		p_secstodate(u_long);
int		dn_count_labels(const char *);
int		dn_comp(const char *, u_char *, int, u_char **, u_char **);
int		dn_expand(const u_char *, const u_char *, const u_char *,
			  char *, int);
u_int		res_randomid(void);
int		res_nameinquery(const char *, int, int, const u_char *,
				const u_char *);
int		res_queriesmatch(const u_char *, const u_char *,
				 const u_char *, const u_char *);
const char *	p_section(int, int);
void		res_send_setqhook(res_send_qhook);
void		res_send_setrhook(res_send_rhook);

/* XXX The following depend on the ns_updrec typedef in arpa/nameser.h */
#ifdef _ARPA_NAMESER_H_
int		res_update (ns_updrec *);
int		res_mkupdate (ns_updrec *, u_char *, int);
ns_updrec *	res_mkupdrec (int, const char *, u_int, u_int, u_long);
void		res_freeupdrec (ns_updrec *);
#endif
__END_DECLS

#endif /* !_RESOLV_H_ */
