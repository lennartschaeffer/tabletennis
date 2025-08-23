import { AppShell, Stack, Title, Text, Flex } from "@mantine/core";
import React from "react";
import { FaTableTennis } from "react-icons/fa";

interface LayoutProps {
  children: React.ReactNode;
}
const Layout = ({ children }: LayoutProps) => {
  return (
    <AppShell
      padding="md"
      header={{ height: 60 }}
      navbar={{
        width: 300,
        breakpoint: "sm",
      }}
    >
      <AppShell.Header>
        <Flex justify="start" align="center" mx={20}>
          <Flex justify="center" gap={10} align="center">
            <Title size={40}>Ping</Title>
            <FaTableTennis size={35} />
          </Flex>
        </Flex>
      </AppShell.Header>

      <AppShell.Navbar>
        <Stack justify="center" align="center" mt={15}>
          <Text>Home</Text>
        </Stack>
      </AppShell.Navbar>

      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
};

export default Layout;
