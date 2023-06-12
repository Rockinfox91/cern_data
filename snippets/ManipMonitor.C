#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
#include <error.h>
#include <stdlib.h>

#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <arpa/inet.h>

#include <ncurses.h>

#include <time.h>

#include "fileUtilities.h"


#define PROG "ManMon"
#define MAX_AXES 4                                   // Umbilical + 3 axes

int main( int argc, char *argv[] )
{

	char buff[ 4096 ], sbuff[ 4096 ], tbuff[ 64 ];

	char *p, *q, *s;
	char *command = NULL;
	char *log_file = NULL;
	char *poly_object = NULL;
	char *m_term = NULL;

	char *Axes[ MAX_AXES + 1 ];                        // Make sure we can NULL terminate list
	char Modes[ MAX_AXES][ 16 ];
	
	int verbose = 0x0;
	int argc1 = 0;
	int sockfd;
	int l, n, i;
	int interval = 500;
	int ibin = 0;
	int Np = 10000;
	int expert = 0x0;
	
	double dt = 100;
	double rl[ MAX_AXES ], ts[ MAX_AXES ], err[ MAX_AXES ], vel[ MAX_AXES ], steps[ MAX_AXES ], stretch[ MAX_AXES],
		z, f, sum, serr;
	double ts_frac;
	double total = -99999999;

	time_t t, t1, t_x;
	useconds_t usec = 10000;
	struct sockaddr_in server_addr;

	struct stat s_buff;
	struct tm tm;

	FILE *fp = NULL;

	
	Opt l_opt[] = {
		{ "-log_file", P_OPT_C, (void *)&log_file },
		{ "-poly_object", P_OPT_C, (void *)&poly_object },
		{ "-interval", P_OPT_L_DEC, (void *)&interval },
		{ "-command", P_OPT_C, (void *)&command },
		{ "-time", P_OPT_D, (void *)&dt },
		{ "-points", P_OPT_L_DEC, (void *)&Np },	
		{ "-verbose", P_OPT_BOOL, (void *)&verbose },
		{ "-total", P_OPT_D, (void *)&total },
		{ "-expert", P_OPT_BOOL, (void *)&expert },
		{ "-terminate", P_OPT_C, (void *)&m_term },
		{ NULL, 0x0, NULL }
	};


	parseOptions( argc, argv, l_opt );

	if( !poly_object ) {
		printf( "%s : No POLY object to monitor\n", PROG );
		return -1;
	}

	if( !command ) {
		printf( "%s : No command defined\n", PROG );
		return -1;
	}
	
	if( interval < 0 ) interval = 10;
	usec = 1000 * interval;

	if( !( sockfd = socket( AF_INET, SOCK_STREAM, 0 ) ) ) {
		printf( "%s : Error opening socket\n", PROG );
		return -1;
	}
	
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons( 1777 );
	server_addr.sin_addr.s_addr = inet_addr( "127.0.0.1" );
	memset( server_addr.sin_zero, '\0', sizeof(server_addr.sin_zero) );  
	l = sizeof(server_addr);
	if( connect( sockfd, (struct sockaddr *)&server_addr, l ) < 0 ) {
		printf( "%s : Error connecting on socket 1777\n", PROG );
		return -1;
	}


	l = recv( sockfd, buff, sizeof(buff), 0 );
	if( sizeof(buff) - 1 < l ) l = sizeof(buff) - 1;
	buff[ l ] = 0x0;
	printf( "%s : %s\n", PROG, buff );

	if( sizeof(sbuff) - 2 < strlen( command ) ) {                          // We may need room for up to two more characters
		printf( "%s : Command buffer overflow\n" );
		return -1;
	}
	
	fp = stdout;

	if( log_file ) {
		if( !( fp = fopen( log_file, "w" ) ) ) {
			printf( "%s : Error opening log file\n", PROG );
			return -1;
		}
	}

	Axes[ 0 ] = NULL;

	initscr();

	strcpy( sbuff, poly_object );
	strcat( sbuff, " monitor\n" );
	l = strlen( sbuff );;
	send( sockfd, sbuff, l, 0 );
	l = recv( sockfd, buff, sizeof(buff) - 1, 0 );                      // Don't use entire buffer 
	buff[ l ] = 0x0;                                                    // - and make sure we're terminated

	if( !( p = strstr( buff, "Axes:" ) ) ) {
		printf( "%s : No axes found !\n", PROG );
		return -1;
	}

	while( *p != ' ' && *p != '\n' && *p != '\t' ) ++p;                 // Look for keyword
	if( *p == '\n' ) {
		printf( "%s : No axes found !\n", PROG );                         // Found \n so line was empty
		return -1;
	}

	q = p;
	while( *q != '\n' ) ++q;
	*q = 0x0;                                                           // Terminate buffer
	n = 0;
	while( 1 ) {                                                        // Look for axes
		if( !( q = strtok( p, "\t " ) ) ) break;
		printf( "Axis[%d] : %s\n", n, q );
		Axes[ n ]= (char *)malloc( strlen( q ) + 1 );
		strcpy( Axes[ n ], q );
		++n;
		Axes[ n ] = NULL;
		p = NULL;
	}

	
	time( &t );
	dt += t;
	t_x = t + 600;
	
	while( 1 ) {
		
		time( &t );
		if( dt < t ) break;

		if( m_term ) {
			if( !stat( m_term, &s_buff ) ) {
				endwin();
				printf( "Forced stop\n" );
				break;
			}
		}

		if( t_x < t && expert ) {
			send( sockfd, "expert room601\n", 15, 0 );
			recv( sockfd, buff, sizeof(buff), 0 );
			time( &t_x );
			t_x += 600;
		}

		strcpy( sbuff, command );
		n = strlen( sbuff );

		if( sbuff[ n - 1 ] != '\n' ) {
			sbuff[ n ] = '\n';
			sbuff[ n + 1 ] = 0x0;
			++n;
		}

		l = send( sockfd, sbuff, n, 0 );

		l = recv( sockfd, buff, sizeof(buff) - 1, 0 );
		buff[ l ] = 0x0;

		if( verbose ) { 
			fprintf( fp, "Sample [%d] :  %s\n", ibin, buff );
		} else {
			//			fprintf( fp, "Sample [%d]\n", ibin );
		}			
		++ibin;

		for( ;; ) {
			p = buff;

			if( !( p = strstr( p, "Time:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			strcpy( tbuff, q );

			s = strtok( q, "\t " );
			*( s + 4 ) = 0x0;
			tm.tm_year = atol( s ) - 1900;
			s += 5;
			*( s + 2 ) = 0x0;
			tm.tm_mon = atol( s ) - 1;
			s += 3;
			*( s + 2 ) = 0x0;
			tm.tm_mday = atol( s );

			s = strtok( NULL, "\t " );
			*( s + 2 ) = 0x0;
			tm.tm_hour = atol( s );
			s += 3;
			*( s + 2 ) = 0x0;
			tm.tm_min = atol( s );
			s += 3;
			*( s + 2 ) = 0x0;
			tm.tm_sec = atol( s );
			s += 3;
			*( s + 2 ) = 0x0;
			ts_frac = atol( s ) * 0.01;

			s = strtok( NULL, "\t " );
			if( !strcmp( s, "DST" ) ) tm.tm_isdst = 1;
			t1 = mktime( &tm );

			if( !( p = strstr( p, "Status:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			s = strtok( q, "\t " );

			if( !( p = strstr( p, "Position:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			strtok( q, "\t " );
			strtok( NULL, "\t " );
			s = strtok( NULL, "\t " );
			z = atof( s );

			if( !( p = strstr( p, "Net Force:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			strtok( q, "\t " );
			strtok( NULL, "\t " );
			s = strtok( NULL, "\t " );
			f = atof( s );

			if( !( p = strstr( p, "Length Error:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			s = strtok( q, "\t " );
			serr = atof( s );
			
			if( ! ( p = strstr( p, "Axes:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			s = strtok( q, "\t " );
			for( n=0; n<MAX_AXES; ++n ) {
				if( !Axes[ n ] ) break;
				if( strcmp( s, Axes[ n ] ) ) {
					printf( "%S : Axis mismatch : expected %s, got %s\n", PROG, Axes[ n ], s );    // ***** fix
					p = NULL;
					break;
				}
				s = strtok( NULL, "\t " );
			}

			if( ! ( p = strstr( p, "Lengths:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			s = strtok( q, "\t " );
			for( n=0; n<MAX_AXES; ++n ) {
				if( !Axes[ n ] ) break;
				rl[ n ] = atof( s );
				s = strtok( NULL, "\t " );
			}

			if( ! ( p = strstr( p, "Modes:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			s = strtok( q, "\t " );
			for( n=0; n<MAX_AXES; ++n ) {
				if( !Axes[ n ] ) break;
				strcpy( &Modes[ n ][ 0 ], s );
				s = strtok( NULL, "\t " );
			}

			if( ! ( p = strstr( p, "Tensions:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			s = strtok( q, "\t " );
			for( n=0; n<MAX_AXES; ++n ) {
				if( !Axes[ n ] ) break;
				ts[ n ] = atof( s );
				s = strtok( NULL, "\t " );
			}

			if( ! ( p = strstr( p, "Encoder Errors:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			s = strtok( q, "\t " );
			for( n=0; n<MAX_AXES; ++n ) {
				if( !Axes[ n ] ) break;
				err[ n ] = atof( s );
				s = strtok( NULL, "\t " );
			}

			if( ! ( p = strstr( p, "Velocities:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			s = strtok( q, "\t " );
			for( n=0; n<MAX_AXES; ++n ) {
				if( !Axes[ n ] ) break;
				vel[ n ] = atof( s );
				s = strtok( NULL, "\t " );
			}

			if( ! ( p = strstr( p, "Motors:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			s = strtok( q, "\t " );
			for( n=0; n<MAX_AXES; ++n ) {
				if( !Axes[ n ] ) break;
				steps[ n ] = atof( s );
				s = strtok( NULL, "\t " );
			}

			if( ! ( p = strstr( p, "Stretch:" ) ) ) break;
			q = p;
			while( *p != '\n' ) ++p;
			*p = 0x0;
			++p;
			while( *q != ':' ) ++q;
			++q;
			s = strtok( q, "\t " );
			for( n=0; n<MAX_AXES; ++n ) {
				if( !Axes[ n ] ) break;
				stretch[ n ] = atof( s );
				s = strtok( NULL, "\t " );
			}
		
			break;
		}
		
		if( !p ) {
			printf( "Error decoding data\n" );
		}

		sum = 0;
		for( n=0; n<MAX_AXES; ++n ) {
			if( !Axes[ n ] ) break;

			sum += rl[ n ];
		}

		mvprintw( 1, 1, "                     PolyAxis: %s\n", poly_object );

		for( n=0; n<MAX_AXES; ++n ) {
			if( !Axes[ n ] ) break;
			printw( "       %s             ", Axes[ n ] );
		}
		printw( "\n" );

		for( n=0; n<MAX_AXES; ++n ) {
			if( !Axes[ n ] ) break;
			printw( "   Mode:       %s       ", &Modes[ n ][ 0 ] );
		}
		printw( "\n" );

		for( n=0; n<MAX_AXES; ++n ) {
			if( !Axes[ n ] ) break;
			printw( "   Tension(N):  %7.2lf   ", ts[ n ] );
		}
		printw( "\n\n" );

		for( n=0; n<MAX_AXES; ++n ) {
			if( !Axes[ n ] ) break;
			printw( "   Length(cm):  %7.2lf   ", rl[ n ] );
		}
		printw( "\n\n" );

		for( n=0; n<MAX_AXES; ++n ) {
			if( !Axes[ n ] ) break;
			printw( "   Error(cm):   %7.2lf   ", err[ n ] );
		}
		printw( "\n\n" );

		printw( "                       X            Y            Z\n" );
		printw( "   Source Position:    0.00         0.00      %7.2lf\n", z );
		printw( "   Time:            %s\n", tbuff );
		printw( "   Length Error:      %7.2lf      Net Force: %7.2lf\n", serr, f );
		printw( "\n" );

		for( n=0; n<MAX_AXES; ++n ) {
			if( !Axes[ n ] ) break;
		printw( "   Velocities:  %7.2lf   ", vel[ n ] );
		}
		printw( "\n" );

		for( n=0; n<MAX_AXES; ++n ) {
			if( !Axes[ n ] ) break;
			printw( "   Steps:       %7.2lf   ", steps[ n ] );
		}
		printw( "\n" );

		for( n=0; n<MAX_AXES; ++n ) {
			if( !Axes[ n ] ) break;
			printw( "   Stretch:     %7.2lf   ", stretch[ n ] );
		}
		printw( "\n" );

		refresh();

		usleep( usec );
		
	}

	if( log_file ) fclose( fp );

	endwin();
	printf( "%s : Time out\n", PROG );

	printf( "done ...\n" );

}
