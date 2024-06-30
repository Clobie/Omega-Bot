const { GameDig } = require('gamedig');

async function queryServer(name, type, host, port) {
    try {
        const state = await GameDig.query({
            type: type,
            host: host,
            port: port
        });
        return {
            name: name,
            status: 'online',
            players: state.players.length,
            maxPlayers: state.maxplayers
        };
    } catch (error) {
        return {
            name: name,
            status: 'offline',
            players: 0,
            maxPlayers: 0
        };
    }
}

async function main() {
    const servers = [
        { name: "Digger's Paradise", type: 'valheim', host: '192.168.1.151', port: 2456 },
        { name: "Digger's Paradise Vanilla", type: 'valheim', host: '192.168.1.150', port: 2458 },
        { name: "Clobie's Bedrock", type: 'minecraft', host: '192.168.1.102', port: 19132 }
    ];

    const results = [];
    for (const server of servers) {
        const result = await queryServer(server.name, server.type, server.host, server.port);
        results.push(result);
    }

    console.log(JSON.stringify(results));
}

main();
